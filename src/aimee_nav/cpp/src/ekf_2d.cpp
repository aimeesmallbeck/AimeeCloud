#include "aimee_nav_core/ekf_2d.hpp"
#include <cmath>
#include <cstring>

namespace aimee_nav_core {

EKF2D::EKF2D() {
    reset(0.0f, 0.0f, 0.0f);
    // Process noise
    Q_[0] = 0.01f; Q_[1] = 0.0f;  Q_[2] = 0.0f;
    Q_[3] = 0.0f;  Q_[4] = 0.01f; Q_[5] = 0.0f;
    Q_[6] = 0.0f;  Q_[7] = 0.0f;  Q_[8] = 0.02f;
}

void EKF2D::reset(float x, float y, float theta) {
    state_[0] = x; state_[1] = y; state_[2] = theta;
    P_[0] = 0.1f; P_[1] = 0.0f;  P_[2] = 0.0f;
    P_[3] = 0.0f; P_[4] = 0.1f;  P_[5] = 0.0f;
    P_[6] = 0.0f; P_[7] = 0.0f;  P_[8] = 0.1f;
}

void EKF2D::predict(float v, float w, float dt) {
    float x = state_[0];
    float y = state_[1];
    float th = state_[2];

    if (std::abs(w) < 1e-3f) {
        state_[0] = x + v * dt * std::cos(th);
        state_[1] = y + v * dt * std::sin(th);
    } else {
        float r = v / w;
        state_[0] = x - r * std::sin(th) + r * std::sin(th + w * dt);
        state_[1] = y + r * std::cos(th) - r * std::cos(th + w * dt);
        state_[2] = th + w * dt;
    }

    // Jacobian F (simplified, identity + velocity terms)
    float F[9] = {
        1.0f, 0.0f, -v * dt * std::sin(th),
        0.0f, 1.0f,  v * dt * std::cos(th),
        0.0f, 0.0f,  1.0f
    };

    // P = F*P*F^T + Q  (simplified, only diagonal propagation for speed)
    float newP[9];
    for (int i = 0; i < 3; ++i) {
        for (int j = 0; j < 3; ++j) {
            newP[i*3+j] = Q_[i*3+j];
            for (int k = 0; k < 3; ++k) {
                newP[i*3+j] += F[i*3+k] * P_[k*3+j];
            }
        }
    }
    std::memcpy(P_.data(), newP, sizeof(newP));
}

void EKF2D::update_imu_yaw(float yaw, float yaw_variance) {
    float y = yaw - state_[2];
    while (y > M_PI) y -= 2.0f * M_PI;
    while (y < -M_PI) y += 2.0f * M_PI;

    float s = P_[8] + yaw_variance;
    float k = P_[8] / s;
    state_[2] += k * y;
    while (state_[2] > M_PI) state_[2] -= 2.0f * M_PI;
    while (state_[2] < -M_PI) state_[2] += 2.0f * M_PI;
    P_[8] = (1.0f - k) * P_[8];
}

void EKF2D::update_scan_pose(float x, float y, float theta,
                             float pos_variance, float yaw_variance) {
    // Update x
    float sx = P_[0] + pos_variance;
    float kx = P_[0] / sx;
    state_[0] += kx * (x - state_[0]);
    P_[0] = (1.0f - kx) * P_[0];

    // Update y
    float sy = P_[4] + pos_variance;
    float ky = P_[4] / sy;
    state_[1] += ky * (y - state_[1]);
    P_[4] = (1.0f - ky) * P_[4];

    // Update theta
    float y_err = theta - state_[2];
    while (y_err > M_PI) y_err -= 2.0f * M_PI;
    while (y_err < -M_PI) y_err += 2.0f * M_PI;
    float st = P_[8] + yaw_variance;
    float kt = P_[8] / st;
    state_[2] += kt * y_err;
    while (state_[2] > M_PI) state_[2] -= 2.0f * M_PI;
    while (state_[2] < -M_PI) state_[2] += 2.0f * M_PI;
    P_[8] = (1.0f - kt) * P_[8];
}

} // namespace aimee_nav_core
