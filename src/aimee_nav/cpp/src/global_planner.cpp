#include "aimee_nav_core/global_planner.hpp"
#include "aimee_nav_core/grid_map.hpp"
#include <queue>
#include <cmath>
#include <algorithm>

namespace aimee_nav_core {

GlobalPlanner::GlobalPlanner() = default;

std::vector<std::pair<float, float>> GlobalPlanner::plan(
    const GridMap& map,
    float start_x, float start_y,
    float goal_x, float goal_y) {

    int sx, sy, gx, gy;
    if (!map.world_to_grid(start_x, start_y, sx, sy) ||
        !map.world_to_grid(goal_x, goal_y, gx, gy)) {
        return {};
    }

    int w = map.width_cells();
    int h = map.height_cells();
    int size = w * h;

    std::vector<int> gscore(size, -1);
    std::vector<float> fscore(size, 1e9f);
    std::vector<int> parent(size, -1);
    std::vector<bool> closed(size, false);

    auto idx = [w](int x, int y) { return y * w + x; };

    using PQNode = std::pair<float, int>;
    std::priority_queue<PQNode, std::vector<PQNode>, std::greater<PQNode>> open;

    int sidx = idx(sx, sy);
    gscore[sidx] = 0;
    fscore[sidx] = 0.0f;
    open.emplace(0.0f, sidx);

    const int dirs[8][2] = {{1,0},{-1,0},{0,1},{0,-1},{1,1},{1,-1},{-1,1},{-1,-1}};
    const float dcost[8] = {1.0f, 1.0f, 1.0f, 1.0f, 1.414f, 1.414f, 1.414f, 1.414f};

    while (!open.empty()) {
        auto [f, cidx] = open.top();
        open.pop();
        if (closed[cidx]) continue;
        closed[cidx] = true;

        int cx = cidx % w;
        int cy = cidx / w;

        if (cx == gx && cy == gy) {
            // Reconstruct path
            std::vector<std::pair<int,int>> path_cells;
            int cur = cidx;
            while (cur >= 0) {
                path_cells.emplace_back(cur % w, cur / w);
                cur = parent[cur];
            }
            std::reverse(path_cells.begin(), path_cells.end());

            // Smooth with line-of-sight
            std::vector<std::pair<int,int>> smoothed;
            smoothed.push_back(path_cells.front());
            size_t i = 0;
            while (i < path_cells.size() - 1) {
                size_t j = path_cells.size() - 1;
                for (; j > i + 1; --j) {
                    int x0 = smoothed.back().first;
                    int y0 = smoothed.back().second;
                    int x1 = path_cells[j].first;
                    int y1 = path_cells[j].second;
                    bool clear = true;
                    int dx = std::abs(x1 - x0);
                    int dy = std::abs(y1 - y0);
                    int sx_ = (x0 < x1) ? 1 : -1;
                    int sy_ = (y0 < y1) ? 1 : -1;
                    int err_ = dx - dy;
                    int xx = x0, yy = y0;
                    while (true) {
                        if (xx == x1 && yy == y1) break;
                        if (map.inflated_cell(xx, yy) >= 50) { clear = false; break; }
                        int e2 = 2 * err_;
                        if (e2 > -dy) { err_ -= dy; xx += sx_; }
                        if (e2 < dx) { err_ += dx; yy += sy_; }
                    }
                    if (clear) { i = j; smoothed.push_back(path_cells[j]); break; }
                }
                if (j == i + 1) {
                    smoothed.push_back(path_cells[i + 1]);
                    ++i;
                }
            }

            std::vector<std::pair<float, float>> path;
            for (const auto& p : smoothed) {
                float wx, wy;
                map.grid_to_world(p.first, p.second, wx, wy);
                path.emplace_back(wx, wy);
            }
            return path;
        }

        for (int d = 0; d < 8; ++d) {
            int nx = cx + dirs[d][0];
            int ny = cy + dirs[d][1];
            if (nx < 0 || nx >= w || ny < 0 || ny >= h) continue;
            int nidx_ = idx(nx, ny);
            if (closed[nidx_]) continue;
            if (map.inflated_cell(nx, ny) >= 50) continue;

            int tentative_g = gscore[cidx] + static_cast<int>(dcost[d] * 10.0f);
            if (gscore[nidx_] < 0 || tentative_g < gscore[nidx_]) {
                gscore[nidx_] = tentative_g;
                float h = std::hypot(static_cast<float>(gx - nx), static_cast<float>(gy - ny));
                fscore[nidx_] = tentative_g / 10.0f + h;
                parent[nidx_] = cidx;
                open.emplace(fscore[nidx_], nidx_);
            }
        }
    }

    return {};
}

} // namespace aimee_nav_core
