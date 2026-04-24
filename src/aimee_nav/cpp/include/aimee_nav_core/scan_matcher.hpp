#pragma once

#include <vector>
#include <tuple>
#include <memory>
#include "aimee_nav_core/grid_map.hpp"

namespace aimee_nav_core {

/**
 * @brief Multi-resolution grid-correlation scan matcher.
 *
 * Localizes a 2D lidar scan against an occupancy grid by correlating
 * hit points with the grid map.
 */
class ScanMatcher {
public:
    explicit ScanMatcher(const GridMap& map);

    /** Match a scan against the current map.
     *
     * @param ranges            Scan ranges (m)
     * @param angle_min         Start angle (rad)
     * @param angle_increment   Angle step (rad)
     * @param range_min         Min valid range
     * @param range_max         Max valid range
     * @param initial_x         Initial guess x (m)
     * @param initial_y         Initial guess y (m)
     * @param initial_theta     Initial guess theta (rad)
     * @param search_radius_m   Search radius around initial guess (m)
     * @param search_angle_rad  Search angle around initial guess (rad)
     *
     * @return tuple(best_x, best_y, best_theta, match_score)
     *         score > 0 means good match; <= 0 means failure.
     */
    std::tuple<float, float, float, float> match(
        const std::vector<float>& ranges,
        float angle_min, float angle_increment,
        float range_min, float range_max,
        float initial_x, float initial_y, float initial_theta,
        float search_radius_m = 0.5f,
        float search_angle_rad = 0.2f) const;

private:
    const GridMap& map_;

    float score_pose(float x, float y, float theta,
                     const std::vector<float>& xs,
                     const std::vector<float>& ys) const;
};

} // namespace aimee_nav_core
