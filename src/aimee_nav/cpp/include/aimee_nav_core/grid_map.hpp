#pragma once

#include <cstdint>
#include <vector>
#include <memory>
#include <tuple>

namespace aimee_nav_core {

class GridMap {
public:
    GridMap(float width_m, float height_m, float resolution_m, float inflation_radius_m);
    ~GridMap() = default;

    GridMap(const GridMap&) = default;
    GridMap& operator=(const GridMap&) = default;
    GridMap(GridMap&&) = default;
    GridMap& operator=(GridMap&&) = default;

    void clear();

    void update_from_scan(float origin_x, float origin_y, float origin_theta,
                          const std::vector<float>& ranges,
                          float angle_min, float angle_increment,
                          float range_min, float range_max);

    void inflate_obstacles();

    std::vector<uint8_t> extract_local_costmap(float cx, float cy,
                                                float window_width_m,
                                                float window_height_m) const;

    /** Extract a sub-grid centered at (cx, cy) in world coordinates. */
    GridMap extract_local_grid_map(float cx, float cy,
                                    float window_width_m,
                                    float window_height_m) const;

    float width_m() const { return width_m_; }
    float height_m() const { return height_m_; }
    float resolution_m() const { return resolution_m_; }
    int width_cells() const { return width_cells_; }
    int height_cells() const { return height_cells_; }

    bool world_to_grid(float wx, float wy, int& gx, int& gy) const;
    void grid_to_world(int gx, int gy, float& wx, float& wy) const;

    int8_t cell(int gx, int gy) const;
    void set_cell(int gx, int gy, int8_t value);

    uint8_t inflated_cell(int gx, int gy) const;

    const std::vector<int8_t>& data() const { return grid_; }
    const std::vector<uint8_t>& inflated_data() const { return inflated_grid_; }

    void set_origin(float origin_x, float origin_y);
    float origin_x() const { return origin_x_; }
    float origin_y() const { return origin_y_; }

private:
    float width_m_, height_m_, resolution_m_, inflation_radius_m_;
    int width_cells_, height_cells_;
    float origin_x_ = 0.0f, origin_y_ = 0.0f;

    std::vector<int8_t> grid_;
    std::vector<uint8_t> inflated_grid_;

    void bresenham_line(int x0, int y0, int x1, int y1,
                        std::vector<std::pair<int,int>>& out) const;
};

} // namespace aimee_nav_core
