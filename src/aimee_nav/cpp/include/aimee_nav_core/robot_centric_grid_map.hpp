#pragma once

#include <cstdint>
#include <vector>

namespace aimee_nav_core {

/**
 * @brief Robot-centric occupancy grid with decay and inflation.
 *
 * Semantics match LocalGridMap:
 *   0   = unknown
 *   1-99 = free (higher = more recently observed)
 *   100-127 = occupied
 */
class RobotCentricGridMap {
public:
    RobotCentricGridMap(float size_m, float resolution_m, float inflation_m,
                        float decay_time_s = 10.0f);

    void clear();

    /** Update grid from a lidar scan. Robot-centric coordinates. */
    void update_from_scan(
        const std::vector<float>& ranges,
        const std::vector<float>& angles_deg,
        float robot_x, float robot_y, float robot_theta,
        float max_range_m = 8.0f);

    /** Apply temporal decay. Call before update_from_scan. */
    void decay();

    /** Get raw grid data as flat vector (row-major). */
    const std::vector<int8_t>& data() const { return grid_; }

    int grid_size() const { return grid_size_; }
    float resolution() const { return resolution_; }
    float size_m() const { return size_m_; }

    float origin_x() const { return origin_x_; }
    float origin_y() const { return origin_y_; }
    float origin_theta() const { return origin_theta_; }

private:
    float size_m_, resolution_, inflation_m_, decay_time_s_;
    int grid_size_;
    int half_;
    float origin_x_ = 0.0f, origin_y_ = 0.0f, origin_theta_ = 0.0f;
    float last_decay_time_ = 0.0f;

    std::vector<int8_t> grid_;

    void bresenham(int x0, int y0, int x1, int y1,
                   std::vector<std::pair<int,int>>& out) const;
    void mark_obstacle(int row, int col, int inflation_cells);
    inline int idx(int r, int c) const { return r * grid_size_ + c; }
};

} // namespace aimee_nav_core
