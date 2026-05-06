#include <rclcpp/rclcpp.hpp>
#include <aimee_msgs/msg/grasp_pose.hpp>
#include <geometry_msgs/msg/pose.hpp>
#include <std_msgs/msg/string.hpp>

#include <fcntl.h>
#include <termios.h>
#include <unistd.h>
#include <string>
#include <vector>
#include <cmath>

using std::placeholders::_1;

class ArmKinematicsBridge : public rclcpp::Node
{
public:
    ArmKinematicsBridge() : Node("arm_kinematics_bridge")
    {
        this->declare_parameter("stm32_serial_port", "/dev/ttyACM0");
        this->declare_parameter("stm32_baud_rate", 115200);

        std::string port = this->get_parameter("stm32_serial_port").as_string();
        int baud = this->get_parameter("stm32_baud_rate").as_int();

        init_serial(port, baud);

        subscription_ = this->create_subscription<aimee_msgs::msg::GraspPose>(
            "/manipulation/grasp_pose", 10, std::bind(&ArmKinematicsBridge::grasp_pose_callback, this, _1));

        RCLCPP_INFO(this->get_logger(), "Arm Kinematics Bridge initialized. Listening on /manipulation/grasp_pose");
    }

    ~ArmKinematicsBridge()
    {
        if (serial_fd_ >= 0) {
            close(serial_fd_);
        }
    }

private:
    int serial_fd_ = -1;
    rclcpp::Subscription<aimee_msgs::msg::GraspPose>::SharedPtr subscription_;

    void init_serial(const std::string& port, int baud)
    {
        serial_fd_ = open(port.c_str(), O_RDWR | O_NOCTTY | O_NDELAY);
        if (serial_fd_ == -1) {
            RCLCPP_ERROR(this->get_logger(), "Failed to open serial port %s", port.c_str());
            return;
        }

        struct termios options;
        tcgetattr(serial_fd_, &options);

        speed_t speed;
        switch (baud) {
            case 9600: speed = B9600; break;
            case 115200: speed = B115200; break;
            case 921600: speed = B921600; break;
            default: speed = B115200; break;
        }

        cfsetispeed(&options, speed);
        cfsetospeed(&options, speed);

        options.c_cflag |= (CLOCAL | CREAD);
        options.c_cflag &= ~PARENB;
        options.c_cflag &= ~CSTOPB;
        options.c_cflag &= ~CSIZE;
        options.c_cflag |= CS8;
        options.c_iflag &= ~(IXON | IXOFF | IXANY);
        options.c_lflag &= ~(ICANON | ECHO | ECHOE | ISIG);
        options.c_oflag &= ~OPOST;

        tcsetattr(serial_fd_, TCSANOW, &options);
        RCLCPP_INFO(this->get_logger(), "Serial port %s opened at %d baud", port.c_str(), baud);
    }

    // Simplified Inverse Kinematics for ROArm-M3 (Dummy implementation for architecture validation)
    std::vector<int> calculate_ik(const geometry_msgs::msg::Pose& pose, float gripper_width)
    {
        std::vector<int> joints(6, 2047); // Home position for 12-bit servos

        // Base rotation (yaw)
        double yaw = atan2(pose.position.y, pose.position.x);
        joints[0] = 2047 + (int)(yaw * 2048.0 / M_PI);

        // Map X, Y, Z to simplified planar joints (Shoulder, Elbow, Wrist, Roll)
        // This is a placeholder. Real IK involves Trigonometry based on link lengths.
        double distance = sqrt(pose.position.x * pose.position.x + pose.position.y * pose.position.y);
        joints[1] = 2047 + (int)((distance - 0.2) * 1000); // Shoulder
        joints[2] = 2047 - (int)((pose.position.z - 0.1) * 1000); // Elbow
        joints[3] = 2047; // Wrist
        joints[4] = 2047; // Roll

        // Gripper mapping
        joints[5] = 2047 + (int)(gripper_width * 10000);

        // Clamp values to 12-bit range
        for (int& j : joints) {
            if (j < 0) j = 0;
            if (j > 4095) j = 4095;
        }

        return joints;
    }

    void send_waypoint(const std::vector<int>& joints, int duration_ms)
    {
        if (serial_fd_ < 0) return;

        char buffer[128];
        int len = snprintf(buffer, sizeof(buffer), "W:%d,%d,%d,%d,%d,%d,%d\n",
                           joints[0], joints[1], joints[2], joints[3], joints[4], joints[5], duration_ms);
        
        write(serial_fd_, buffer, len);
        RCLCPP_INFO(this->get_logger(), "Sent Waypoint: %s", buffer);
    }

    void grasp_pose_callback(const aimee_msgs::msg::GraspPose::SharedPtr msg)
    {
        RCLCPP_INFO(this->get_logger(), "Received GraspPose for object: %s", msg->object_id.c_str());

        // 5 Major Waypoints: Home -> Approach -> Grasp -> Retract -> Drop

        // 1. Home
        geometry_msgs::msg::Pose home_pose;
        home_pose.position.x = 0.2;
        home_pose.position.y = 0.0;
        home_pose.position.z = 0.3;
        auto wp_home = calculate_ik(home_pose, msg->gripper_open_width);
        send_waypoint(wp_home, 2000);
        usleep(2000000); // Wait for movement (simulated sync)

        // 2. Approach (Pre-Grasp)
        auto wp_approach = calculate_ik(msg->pre_grasp_pose, msg->gripper_open_width);
        send_waypoint(wp_approach, 1500);
        usleep(1500000);

        // 3. Grasp
        auto wp_grasp = calculate_ik(msg->grasp_pose, msg->gripper_close_width);
        send_waypoint(wp_grasp, 1000);
        usleep(1000000);

        // 4. Retract (Lift)
        auto wp_retract = calculate_ik(msg->lift_pose, msg->gripper_close_width);
        send_waypoint(wp_retract, 1500);
        usleep(1500000);

        // 5. Drop
        geometry_msgs::msg::Pose drop_pose = home_pose; // Drop at home for now
        auto wp_drop = calculate_ik(drop_pose, msg->gripper_open_width);
        send_waypoint(wp_drop, 2000);
        usleep(2000000);

        RCLCPP_INFO(this->get_logger(), "Maneuver sent to STM32 successfully.");
    }
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<ArmKinematicsBridge>());
    rclcpp::shutdown();
    return 0;
}
