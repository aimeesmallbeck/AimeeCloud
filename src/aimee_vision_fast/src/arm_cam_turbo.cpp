#include <memory>
#include <string>
#include <vector>
#include <thread>
#include <mutex>
#include <atomic>

#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/image.hpp"
#include "sensor_msgs/msg/compressed_image.hpp"
#include "std_srvs/srv/set_bool.hpp"

#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <sys/mman.h>
#include <linux/videodev2.h>

/**
 * ArmCamTurbo: High-efficiency C++ node for the Arm End Effector Camera.
 * 
 * Optimized for RK3588S (Arduino UNO Q) and USB 2.0 bottlenecks.
 * - Uses direct V4L2 mmap for zero-copy frame access.
 * - Publishes CompressedImage directly from hardware MJPEG (no CPU decode).
 * - Implements an "Active" toggle to yield USB bandwidth to the Astra camera.
 */

class ArmCamTurbo : public rclcpp::Node {
public:
    ArmCamTurbo() : Node("arm_cam_turbo") {
        this->declare_parameter("video_device", "/dev/video0");
        this->declare_parameter("width", 640);
        this->declare_parameter("height", 480);
        this->declare_parameter("fps", 15);
        this->declare_parameter("auto_start", false);

        device_name_ = this->get_parameter("video_device").as_string();
        width_ = this->get_parameter("width").as_int();
        height_ = this->get_parameter("height").as_int();
        fps_ = this->get_parameter("fps").as_int();
        is_active_ = this->get_parameter("auto_start").as_bool();

        pub_compressed_ = this->create_publisher<sensor_msgs::msg::CompressedImage>(
            "/vision/arm_camera/image_raw/compressed", 10);

        srv_active_ = this->create_service<std_srvs::srv::SetBool>(
            "~/set_active",
            std::bind(&ArmCamTurbo::handle_set_active, this, std::placeholders::_1, std::placeholders::_2));

        timer_ = this->create_wall_timer(
            std::chrono::milliseconds(1000 / fps_),
            std::bind(&ArmCamTurbo::timer_callback, this));

        if (is_active_) {
            start_capture();
        }

        RCLCPP_INFO(this->get_logger(), "ArmCamTurbo initialized on %s (%dx%d @ %d fps). Status: %s",
            device_name_.c_str(), width_, height_, fps_, is_active_ ? "ACTIVE" : "STANDBY");
    }

    ~ArmCamTurbo() {
        stop_capture();
    }

private:
    void handle_set_active(const std::shared_ptr<std_srvs::srv::SetBool::Request> request,
                          std::shared_ptr<std_srvs::srv::SetBool::Response> response) {
        if (request->data == is_active_) {
            response->success = true;
            response->message = "Already in requested state";
            return;
        }

        if (request->data) {
            if (start_capture()) {
                is_active_ = true;
                response->success = true;
                response->message = "Camera started - Astra should be suspended";
            } else {
                response->success = false;
                response->message = "Failed to open camera device";
            }
        } else {
            stop_capture();
            is_active_ = false;
            response->success = true;
            response->message = "Camera stopped - USB bus cleared for Astra";
        }
    }

    bool start_capture() {
        fd_ = open(device_name_.c_str(), O_RDWR | O_NONBLOCK);
        if (fd_ < 0) {
            RCLCPP_ERROR(this->get_logger(), "Failed to open device: %s", device_name_.c_str());
            return false;
        }

        v4l2_format fmt = {};
        fmt.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
        fmt.fmt.pix.width = width_;
        fmt.fmt.pix.height = height_;
        fmt.fmt.pix.pixelformat = V4L2_PIX_FMT_MJPEG;
        fmt.fmt.pix.field = V4L2_FIELD_ANY;

        if (ioctl(fd_, VIDIOC_S_FMT, &fmt) < 0) {
            RCLCPP_ERROR(this->get_logger(), "Failed to set format to MJPEG");
            close(fd_);
            fd_ = -1;
            return false;
        }

        v4l2_requestbuffers req = {};
        req.count = 4;
        req.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
        req.memory = V4L2_MEMORY_MMAP;

        if (ioctl(fd_, VIDIOC_REQBUFS, &req) < 0) {
            RCLCPP_ERROR(this->get_logger(), "Failed to request buffers");
            close(fd_);
            fd_ = -1;
            return false;
        }

        for (unsigned int i = 0; i < req.count; ++i) {
            v4l2_buffer buf = {};
            buf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
            buf.memory = V4L2_MEMORY_MMAP;
            buf.index = i;

            if (ioctl(fd_, VIDIOC_QUERYBUF, &buf) < 0) {
                RCLCPP_ERROR(this->get_logger(), "Failed to query buffer %d", i);
                return false;
            }

            void* ptr = mmap(NULL, buf.length, PROT_READ | PROT_WRITE, MAP_SHARED, fd_, buf.m.offset);
            if (ptr == MAP_FAILED) {
                RCLCPP_ERROR(this->get_logger(), "mmap failed");
                return false;
            }
            buffers_.push_back({ptr, buf.length});

            if (ioctl(fd_, VIDIOC_QBUF, &buf) < 0) {
                RCLCPP_ERROR(this->get_logger(), "Failed to queue buffer");
                return false;
            }
        }

        v4l2_buf_type type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
        if (ioctl(fd_, VIDIOC_STREAMON, &type) < 0) {
            RCLCPP_ERROR(this->get_logger(), "Failed to start streaming");
            return false;
        }

        return true;
    }

    void stop_capture() {
        if (fd_ < 0) return;

        v4l2_buf_type type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
        ioctl(fd_, VIDIOC_STREAMOFF, &type);

        for (auto& b : buffers_) {
            munmap(b.ptr, b.length);
        }
        buffers_.clear();
        close(fd_);
        fd_ = -1;
    }

    void timer_callback() {
        if (!is_active_ || fd_ < 0) return;

        v4l2_buffer buf = {};
        buf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
        buf.memory = V4L2_MEMORY_MMAP;

        if (ioctl(fd_, VIDIOC_DQBUF, &buf) < 0) {
            return; // No frame ready
        }

        auto msg = std::make_unique<sensor_msgs::msg::CompressedImage>();
        msg->header.stamp = this->now();
        msg->header.frame_id = "arm_camera_optical_frame";
        msg->format = "jpeg";
        
        unsigned char* data_ptr = static_cast<unsigned char*>(buffers_[buf.index].ptr);
        msg->data.assign(data_ptr, data_ptr + buf.bytesused);

        pub_compressed_->publish(std::move(msg));

        ioctl(fd_, VIDIOC_QBUF, &buf);
    }

    struct Buffer {
        void* ptr;
        size_t length;
    };

    std::string device_name_;
    int width_, height_, fps_;
    std::atomic<bool> is_active_;
    int fd_ = -1;
    std::vector<Buffer> buffers_;

    rclcpp::Publisher<sensor_msgs::msg::CompressedImage>::SharedPtr pub_compressed_;
    rclcpp::Service<std_srvs::srv::SetBool>::SharedPtr srv_active_;
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<ArmCamTurbo>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
