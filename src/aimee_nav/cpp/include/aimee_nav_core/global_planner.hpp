#pragma once

#include <vector>
#include <tuple>
#include <cstdint>

namespace aimee_nav_core {

class GridMap;

/**
 * @brief A* global planner on an 8-connected grid.
 */
class GlobalPlanner {
public:
    GlobalPlanner();

    /** Plan a path from start to goal (world coordinates).
     *
     * @param map       Occupancy grid (uses inflated cells)
     * @param start_x   Start x (m)
     * @param start_y   Start y (m)
     * @param goal_x    Goal x (m)
     * @param goal_y    Goal y (m)
     *
     * @return vector of (x,y) waypoints in world coordinates.
     *         Empty if no path found.
     */
    std::vector<std::pair<float, float>> plan(
        const GridMap& map,
        float start_x, float start_y,
        float goal_x, float goal_y);

private:
    struct Node {
        int g = 0;
        float f = 0.0f;
        int parent = -1;
    };
};

} // namespace aimee_nav_core
