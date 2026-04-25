#pragma once

#include <array>

namespace aimee_nav_core {

/**
 * @brief Lightweight 2D EKF for differential-drive pose estimation.
 *
 * State: [x, y, theta]
 * Prediction: cmd_vel (v, w) integration
 * Updates: IMU yaw, scan matcher pose
 */
class EKF2D {
public:
    EKF2D();

    /** Reset state and covariance. */
    void reset(float x, float y, float theta);

    /** Predict step using commanded velocities. */
    void predict(float v, float w, float dt);

    /** Update with IMU yaw measurement (direct theta). */
    void update_imu_yaw(float yaw, float yaw_variance);

    /** Update with scan matcher pose [x, y, theta]. */
    void update_scan_pose(float x, float y, float theta,
                          float pos_variance, float yaw_variance);

    // State access
    float x() const { return state_[0]; }
    float y() const { return state_[1]; }
    float theta() const { return state_[2]; }

    const std::array<float, 9>& covariance() const { return P_; }

private:
    std::array<float, 3> state_ = {0.0f, 0.0f, 0.0f};
    std::array<float, 9> P_ = {};
    std::array<float, 9> Q_ = {}; // process noise
};

} // namespace aimee_nav_core
