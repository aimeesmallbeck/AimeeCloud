#include "aimee_nav_core/dwa_local_planner.hpp"
#include "aimee_nav_core/grid_map.hpp"
#include <cmath>
#include <limits>
#include <algorithm>

namespace aimee_nav_core {

DWALocalPlanner::DWALocalPlanner(const DWAConfig& cfg) : cfg_(cfg) {}

bool DWALocalPlanner::is_collision(const GridMap& map, float x, float y) const {
    int gx, gy;
    if (!map.world_to_grid(x, y, gx, gy)) return true;
    return map.inflated_cell(gx, gy) >= 50;
}

float DWALocalPlanner::obstacle_cost(const GridMap& map, float x, float y) const {
    int gx, gy;
    if (!map.world_to_grid(x, y, gx, gy)) return 0.0f;
    uint8_t c = map.inflated_cell(gx, gy);
    if (c >= 50) return 0.0f;
    return 1.0f - (c / 100.0f);
}

std::tuple<float, float, std::vector<float>, std::vector<float>>
DWALocalPlanner::compute_velocity(
    const GridMap& map,
    float current_x, float current_y, float current_theta,
    float current_v, float current_w,
    const std::vector<std::pair<float, float>>& global_path,
    float goal_x, float goal_y) {

    float best_cost = -std::numeric_limits<float>::infinity();
    float best_v = 0.0f;
    float best_w = 0.0f;
    std::vector<float> best_traj_x, best_traj_y;

    float min_v = std::max(0.0f, current_v - cfg_.acc_lim_x * cfg_.dt);
    float max_v = std::min(cfg_.max_vel_x, current_v + cfg_.acc_lim_x * cfg_.dt);
    float min_w = std::max(-cfg_.max_vel_theta, current_w - cfg_.acc_lim_theta * cfg_.dt);
    float max_w = std::min(cfg_.max_vel_theta, current_w + cfg_.acc_lim_theta * cfg_.dt);

    float nearest_path_x = current_x, nearest_path_y = current_y;
    if (!global_path.empty()) {
        float min_d = std::numeric_limits<float>::max();
        for (const auto& p : global_path) {
            float d = std::hypot(p.first - current_x, p.second - current_y);
            if (d < min_d) {
                min_d = d;
                nearest_path_x = p.first;
                nearest_path_y = p.second;
            }
        }
    }

    for (int iv = 0; iv < cfg_.vx_samples; ++iv) {
        float v = min_v + (max_v - min_v) * static_cast<float>(iv) / std::max(1, cfg_.vx_samples - 1);
        for (int iw = 0; iw < cfg_.vtheta_samples; ++iw) {
            float w = min_w + (max_w - min_w) * static_cast<float>(iw) / std::max(1, cfg_.vtheta_samples - 1);

            // Simulate trajectory
            float x = current_x;
            float y = current_y;
            float th = current_theta;
            float obs_cost = 0.0f;
            bool collision = false;
            int steps = static_cast<int>(cfg_.sim_time / cfg_.dt);

            std::vector<float> traj_x, traj_y;
            traj_x.reserve(steps);
            traj_y.reserve(steps);

            for (int s = 0; s < steps; ++s) {
                if (std::abs(w) < 1e-3f) {
                    x += v * cfg_.dt * std::cos(th);
                    y += v * cfg_.dt * std::sin(th);
                } else {
                    float r = v / w;
                    x += -r * std::sin(th) + r * std::sin(th + w * cfg_.dt);
                    y +=  r * std::cos(th) - r * std::cos(th + w * cfg_.dt);
                    th += w * cfg_.dt;
                }
                traj_x.push_back(x);
                traj_y.push_back(y);

                if (is_collision(map, x, y)) {
                    collision = true;
                    break;
                }
                obs_cost += obstacle_cost(map, x, y);
            }

            if (collision) continue;

            float goal_dx = goal_x - x;
            float goal_dy = goal_y - y;
            float goal_dist = std::hypot(goal_dx, goal_dy);
            float goal_heading = std::atan2(goal_dy, goal_dx);
            float heading_err = std::abs(std::atan2(std::sin(goal_heading - th), std::cos(goal_heading - th)));

            float path_err = std::hypot(x - nearest_path_x, y - nearest_path_y);

            float cost = cfg_.heading_weight * (1.0f - heading_err / M_PI)
                       + cfg_.obstacle_weight * (obs_cost / static_cast<float>(steps))
                       + cfg_.velocity_weight * (v / cfg_.max_vel_x)
                       + cfg_.path_weight * (1.0f / (1.0f + path_err));

            if (cost > best_cost) {
                best_cost = cost;
                best_v = v;
                best_w = w;
                best_traj_x = std::move(traj_x);
                best_traj_y = std::move(traj_y);
            }
        }
    }

    return {best_v, best_w, best_traj_x, best_traj_y};
}

} // namespace aimee_nav_core
