#include "aimee_nav_core/grid_map.hpp"
#include <cmath>
#include <algorithm>
#include <cstring>

namespace aimee_nav_core {

GridMap::GridMap(float width_m, float height_m, float resolution_m, float inflation_radius_m)
    : width_m_(width_m), height_m_(height_m), resolution_m_(resolution_m),
      inflation_radius_m_(inflation_radius_m) {
    width_cells_ = static_cast<int>(std::ceil(width_m / resolution_m));
    height_cells_ = static_cast<int>(std::ceil(height_m / resolution_m));
    grid_.resize(static_cast<size_t>(width_cells_) * height_cells_, -1);
    inflated_grid_.resize(grid_.size(), 255);
}

void GridMap::clear() {
    std::fill(grid_.begin(), grid_.end(), -1);
    std::fill(inflated_grid_.begin(), inflated_grid_.end(), 255);
}

bool GridMap::world_to_grid(float wx, float wy, int& gx, int& gy) const {
    gx = static_cast<int>((wx - origin_x_) / resolution_m_);
    gy = static_cast<int>((wy - origin_y_) / resolution_m_);
    return gx >= 0 && gx < width_cells_ && gy >= 0 && gy < height_cells_;
}

void GridMap::grid_to_world(int gx, int gy, float& wx, float& wy) const {
    wx = origin_x_ + (gx + 0.5f) * resolution_m_;
    wy = origin_y_ + (gy + 0.5f) * resolution_m_;
}

int8_t GridMap::cell(int gx, int gy) const {
    if (gx < 0 || gx >= width_cells_ || gy < 0 || gy >= height_cells_) return -1;
    return grid_[gy * width_cells_ + gx];
}

void GridMap::set_cell(int gx, int gy, int8_t value) {
    if (gx < 0 || gx >= width_cells_ || gy < 0 || gy >= height_cells_) return;
    grid_[gy * width_cells_ + gx] = value;
}

uint8_t GridMap::inflated_cell(int gx, int gy) const {
    if (gx < 0 || gx >= width_cells_ || gy < 0 || gy >= height_cells_) return 255;
    return inflated_grid_[gy * width_cells_ + gx];
}

void GridMap::set_origin(float origin_x, float origin_y) {
    origin_x_ = origin_x;
    origin_y_ = origin_y;
}

void GridMap::bresenham_line(int x0, int y0, int x1, int y1,
                             std::vector<std::pair<int,int>>& out) const {
    int dx = std::abs(x1 - x0);
    int dy = std::abs(y1 - y0);
    int sx = (x0 < x1) ? 1 : -1;
    int sy = (y0 < y1) ? 1 : -1;
    int err = dx - dy;

    while (true) {
        out.emplace_back(x0, y0);
        if (x0 == x1 && y0 == y1) break;
        int e2 = 2 * err;
        if (e2 > -dy) { err -= dy; x0 += sx; }
        if (e2 < dx) { err += dx; y0 += sy; }
    }
}

void GridMap::update_from_scan(float origin_x, float origin_y, float origin_theta,
                               const std::vector<float>& ranges,
                               float angle_min, float angle_increment,
                               float range_min, float range_max) {
    int ox, oy;
    if (!world_to_grid(origin_x, origin_y, ox, oy)) return;

    std::vector<std::pair<int,int>> line;
    line.reserve(1024);

    for (size_t i = 0; i < ranges.size(); ++i) {
        float r = ranges[i];
        if (std::isnan(r) || std::isinf(r) || r < range_min || r > range_max) continue;

        float angle = origin_theta + angle_min + static_cast<float>(i) * angle_increment;
        float hx = origin_x + r * std::cos(angle);
        float hy = origin_y + r * std::sin(angle);

        int gx, gy;
        if (!world_to_grid(hx, hy, gx, gy)) continue;

        line.clear();
        bresenham_line(ox, oy, gx, gy, line);
        for (size_t j = 0; j + 1 < line.size(); ++j) {
            set_cell(line[j].first, line[j].second, 0);
        }
        if (!line.empty()) {
            set_cell(line.back().first, line.back().second, 100);
        }
    }
}

void GridMap::inflate_obstacles() {
    int inflation_cells = static_cast<int>(std::ceil(inflation_radius_m_ / resolution_m_));
    std::fill(inflated_grid_.begin(), inflated_grid_.end(), 0);

    for (int y = 0; y < height_cells_; ++y) {
        for (int x = 0; x < width_cells_; ++x) {
            int idx = y * width_cells_ + x;
            if (grid_[idx] >= 50) {
                for (int dy = -inflation_cells; dy <= inflation_cells; ++dy) {
                    for (int dx = -inflation_cells; dx <= inflation_cells; ++dx) {
                        float dist = std::sqrt(dx*dx + dy*dy) * resolution_m_;
                        if (dist > inflation_radius_m_) continue;
                        int nx = x + dx;
                        int ny = y + dy;
                        if (nx < 0 || nx >= width_cells_ || ny < 0 || ny >= height_cells_) continue;
                        int nidx = ny * width_cells_ + nx;
                        uint8_t cost = static_cast<uint8_t>(100.0f * (1.0f - dist / inflation_radius_m_));
                        if (cost > inflated_grid_[nidx]) {
                            inflated_grid_[nidx] = cost;
                        }
                    }
                }
            }
        }
    }
}

std::vector<uint8_t> GridMap::extract_local_costmap(float cx, float cy,
                                                     float window_width_m,
                                                     float window_height_m) const {
    int wx_cells = static_cast<int>(std::ceil(window_width_m / resolution_m_));
    int wy_cells = static_cast<int>(std::ceil(window_height_m / resolution_m_));
    std::vector<uint8_t> out(static_cast<size_t>(wx_cells) * wy_cells, 255);

    int cx_g, cy_g;
    world_to_grid(cx, cy, cx_g, cy_g);
    int start_x = cx_g - wx_cells / 2;
    int start_y = cy_g - wy_cells / 2;

    for (int y = 0; y < wy_cells; ++y) {
        for (int x = 0; x < wx_cells; ++x) {
            int gx = start_x + x;
            int gy = start_y + y;
            uint8_t val = 255;
            if (gx >= 0 && gx < width_cells_ && gy >= 0 && gy < height_cells_) {
                val = inflated_grid_[gy * width_cells_ + gx];
            }
            out[y * wx_cells + x] = val;
        }
    }
    return out;
}

GridMap GridMap::extract_local_grid_map(float cx, float cy,
                                         float window_width_m,
                                         float window_height_m) const {
    GridMap local(window_width_m, window_height_m, resolution_m_, inflation_radius_m_);
    local.set_origin(cx - window_width_m / 2.0f, cy - window_height_m / 2.0f);

    int lw = local.width_cells();
    int lh = local.height_cells();

    for (int ly = 0; ly < lh; ++ly) {
        for (int lx = 0; lx < lw; ++lx) {
            float wx, wy;
            local.grid_to_world(lx, ly, wx, wy);
            int gx, gy;
            if (world_to_grid(wx, wy, gx, gy)) {
                int idx = gy * width_cells_ + gx;
                if (gx >= 0 && gx < width_cells_ && gy >= 0 && gy < height_cells_) {
                    local.grid_[ly * lw + lx] = grid_[idx];
                    local.inflated_grid_[ly * lw + lx] = inflated_grid_[idx];
                }
            }
        }
    }
    return local;
}

} // namespace aimee_nav_core
