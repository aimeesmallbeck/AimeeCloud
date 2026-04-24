#include "aimee_nav_core/scan_matcher.hpp"
#include <cmath>
#include <limits>

namespace aimee_nav_core {

ScanMatcher::ScanMatcher(const GridMap& map) : map_(map) {}

float ScanMatcher::score_pose(float x, float y, float theta,
                              const std::vector<float>& xs,
                              const std::vector<float>& ys) const {
    float score = 0.0f;
    float c = std::cos(theta);
    float s = std::sin(theta);
    for (size_t i = 0; i < xs.size(); ++i) {
        float lx = xs[i];
        float ly = ys[i];
        float wx = x + c * lx - s * ly;
        float wy = y + s * lx + c * ly;
        int gx, gy;
        if (map_.world_to_grid(wx, wy, gx, gy)) {
            uint8_t cell = map_.inflated_cell(gx, gy);
            // Occupied cells give highest score
            if (cell >= 50) {
                score += 1.0f;
            } else if (cell > 0) {
                score += 0.3f;
            }
            // Unknown cells (255) give 0 score
        }
    }
    return score;
}

std::tuple<float, float, float, float> ScanMatcher::match(
    const std::vector<float>& ranges,
    float angle_min, float angle_increment,
    float range_min, float range_max,
    float initial_x, float initial_y, float initial_theta,
    float search_radius_m, float search_angle_rad) const {

    std::vector<float> xs, ys;
    for (size_t i = 0; i < ranges.size(); ++i) {
        float r = ranges[i];
        if (std::isnan(r) || std::isinf(r) || r < range_min || r > range_max) continue;
        float a = angle_min + static_cast<float>(i) * angle_increment;
        xs.push_back(r * std::cos(a));
        ys.push_back(r * std::sin(a));
    }

    float best_score = -1.0f;
    float best_x = initial_x;
    float best_y = initial_y;
    float best_theta = initial_theta;

    float res = map_.resolution_m();
    int radius_steps = std::max(1, static_cast<int>(search_radius_m / res));
    int angle_steps = std::max(1, static_cast<int>(search_angle_rad / 0.05f));

    for (int ax = -angle_steps; ax <= angle_steps; ++ax) {
        float theta = initial_theta + ax * 0.05f;
        for (int dy = -radius_steps; dy <= radius_steps; ++dy) {
            for (int dx = -radius_steps; dx <= radius_steps; ++dx) {
                float x = initial_x + dx * res;
                float y = initial_y + dy * res;
                float score = score_pose(x, y, theta, xs, ys);
                if (score > best_score) {
                    best_score = score;
                    best_x = x;
                    best_y = y;
                    best_theta = theta;
                }
            }
        }
    }

    return {best_x, best_y, best_theta, best_score};
}

} // namespace aimee_nav_core
