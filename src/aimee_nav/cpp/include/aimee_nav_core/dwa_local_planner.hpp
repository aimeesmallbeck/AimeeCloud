#pragma once

#include <vector>
#include <tuple>
#include <cstdint>

namespace aimee_nav_core {

class GridMap;

/**
 * @brief Simplified Dynamic Window Approach local planner.
 */
struct DWAConfig {
    float max_vel_x = 0.5f;
    float max_vel_theta = 1.5f;
    float acc_lim_x = 1.0f;
    float acc_lim_theta = 2.0f;
    float sim_time = 1.5f;
    float dt = 0.1f;
    int vx_samples = 20;
    int vtheta_samples = 20;
    float goal_distance_tolerance = 0.25f;
    float obstacle_distance_tolerance = 0.15f;
    float heading_weight = 1.0f;
    float obstacle_weight = 10.0f;
    float velocity_weight = 0.5f;
    float path_weight = 1.0f;
};

class DWALocalPlanner {
public:
    explicit DWALocalPlanner(const DWAConfig& cfg = DWAConfig{});

    /** Compute best (v, w) command.
     *
     * @param map               Local costmap (inflated)
     * @param current_x,y,theta Robot pose in map/local frame
     * @param current_v         Current linear velocity
     * @param current_w         Current angular velocity
     * @param global_path       Planned global path waypoints
     * @param goal_x, goal_y    Goal position
     *
     * @return tuple(best_v, best_w, best_trajectory_xs, best_trajectory_ys)
     */
    std::tuple<float, float, std::vector<float>, std::vector<float>> compute_velocity(
        const GridMap& map,
        float current_x, float current_y, float current_theta,
        float current_v, float current_w,
        const std::vector<std::pair<float, float>>& global_path,
        float goal_x, float goal_y);

private:
    DWAConfig cfg_;

    bool is_collision(const GridMap& map, float x, float y) const;
    float obstacle_cost(const GridMap& map, float x, float y) const;
};

} // namespace aimee_nav_core
