#include "aimee_nav_core/robot_centric_grid_map.hpp"
#include <cmath>
#include <algorithm>
#include <ctime>

namespace aimee_nav_core {

RobotCentricGridMap::RobotCentricGridMap(float size_m, float resolution_m, float inflation_m,
                                         float decay_time_s)
    : size_m_(size_m), resolution_(resolution_m), inflation_m_(inflation_m),
      decay_time_s_(decay_time_s) {
    grid_size_ = static_cast<int>(std::round(size_m / resolution_m));
    if (grid_size_ % 2 == 0) ++grid_size_;
    half_ = grid_size_ / 2;
    grid_.resize(static_cast<size_t>(grid_size_) * grid_size_, 0);
}

void RobotCentricGridMap::clear() {
    std::fill(grid_.begin(), grid_.end(), 0);
}

void RobotCentricGridMap::decay() {
    float now = static_cast<float>(std::time(nullptr)); // not ideal; better use clock
    // Actually we should use a monotonic clock, but for simplicity skip time check
    // and just do decay every call if enough time passed.
    // For now, do nothing here; decay will be handled in Python side or simplified.
}

void RobotCentricGridMap::bresenham(int x0, int y0, int x1, int y1,
                                    std::vector<std::pair<int,int>>& out) const {
    int dx = std::abs(x1 - x0);
    int dy = std::abs(y1 - y0);
    int sx = (x0 < x1) ? 1 : -1;
    int sy = (y0 < y1) ? 1 : -1;
    int err = dx - dy;
    while (true) {
        out.emplace_back(y0, x0); // (row, col)
        if (x0 == x1 && y0 == y1) break;
        int e2 = 2 * err;
        if (e2 > -dy) { err -= dy; x0 += sx; }
        if (e2 < dx) { err += dx; y0 += sy; }
    }
}

void RobotCentricGridMap::mark_obstacle(int row, int col, int inflation_cells) {
    for (int dr = -inflation_cells; dr <= inflation_cells; ++dr) {
        for (int dc = -inflation_cells; dc <= inflation_cells; ++dc) {
            if (dr * dr + dc * dc > inflation_cells * inflation_cells) continue;
            int r = row + dr;
            int c = col + dc;
            if (r >= 0 && r < grid_size_ && c >= 0 && c < grid_size_) {
                grid_[idx(r, c)] = 127;
            }
        }
    }
}

void RobotCentricGridMap::update_from_scan(
    const std::vector<float>& ranges,
    const std::vector<float>& angles_deg,
    float robot_x, float robot_y, float robot_theta,
    float max_range_m) {

    origin_x_ = robot_x;
    origin_y_ = robot_y;
    origin_theta_ = robot_theta;

    // Temporal decay (simplified: just reduce all cells slightly)
    for (auto& cell : grid_) {
        if (cell > 0 && cell < 100) {
            cell = std::max<int8_t>(0, cell - 2);
        } else if (cell >= 100) {
            cell = std::max<int8_t>(0, cell - 1);
        }
    }

    int inflation_cells = static_cast<int>(std::round(inflation_m_ / resolution_));
    std::vector<std::pair<int,int>> line;
    line.reserve(1024);

    int robot_row = half_;
    int robot_col = half_;

    for (size_t i = 0; i < ranges.size(); ++i) {
        float dist = ranges[i];
        if (dist <= 0.0f || std::isinf(dist) || std::isnan(dist)) continue;
        if (dist > max_range_m) dist = max_range_m;

        float angle_rad = static_cast<float>(angles_deg[i] * M_PI / 180.0) + robot_theta;
        float end_x = robot_x + dist * std::cos(angle_rad);
        float end_y = robot_y + dist * std::sin(angle_rad);

        // Convert end point to robot-centric grid coords
        float dx = end_x - robot_x;
        float dy = end_y - robot_y;
        float cos_t = std::cos(-robot_theta);
        float sin_t = std::sin(-robot_theta);
        float gx = dx * cos_t - dy * sin_t;
        float gy = dx * sin_t + dy * cos_t;

        int end_col = static_cast<int>(std::round(gx / resolution_)) + half_;
        int end_row = static_cast<int>(std::round(gy / resolution_)) + half_;

        line.clear();
        bresenham(robot_col, robot_row, end_col, end_row, line);

        for (size_t j = 0; j + 1 < line.size(); ++j) {
            int r = line[j].first;
            int c = line[j].second;
            if (r >= 0 && r < grid_size_ && c >= 0 && c < grid_size_) {
                if (grid_[idx(r, c)] < 100) {
                    grid_[idx(r, c)] = std::min<int8_t>(99, std::max<int8_t>(1, grid_[idx(r, c)] + 10));
                }
            }
        }

        if (end_row >= 0 && end_row < grid_size_ && end_col >= 0 && end_col < grid_size_) {
            mark_obstacle(end_row, end_col, inflation_cells);
        }
    }
}

} // namespace aimee_nav_core
