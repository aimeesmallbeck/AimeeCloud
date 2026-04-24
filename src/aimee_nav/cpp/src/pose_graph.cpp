#include "aimee_nav_core/pose_graph.hpp"
#include <cmath>

namespace aimee_nav_core {

int PoseGraph::add_keyframe(const Keyframe& kf) {
    int idx = static_cast<int>(keyframes_.size());
    keyframes_.push_back(kf);
    return idx;
}

std::vector<int> PoseGraph::find_nearby(float x, float y, float radius_m) const {
    std::vector<int> result;
    float r2 = radius_m * radius_m;
    for (int i = 0; i < static_cast<int>(keyframes_.size()); ++i) {
        float dx = keyframes_[i].x - x;
        float dy = keyframes_[i].y - y;
        if (dx*dx + dy*dy < r2) {
            result.push_back(i);
        }
    }
    return result;
}

void PoseGraph::add_constraint(int from, int to, float dx, float dy, float dtheta) {
    constraints_.push_back({from, to, dx, dy, dtheta});
}

void PoseGraph::optimize(int iterations) {
    float alpha = 0.1f;
    for (int it = 0; it < iterations; ++it) {
        for (const auto& c : constraints_) {
            if (c.from < 0 || c.from >= static_cast<int>(keyframes_.size())) continue;
            if (c.to < 0 || c.to >= static_cast<int>(keyframes_.size())) continue;
            auto& from = keyframes_[c.from];
            auto& to = keyframes_[c.to];

            float dx = to.x - from.x;
            float dy = to.y - from.y;
            float dtheta = to.theta - from.theta;
            while (dtheta > M_PI) dtheta -= 2.0f * M_PI;
            while (dtheta < -M_PI) dtheta += 2.0f * M_PI;

            float ex = dx - c.dx;
            float ey = dy - c.dy;
            float et = dtheta - c.dtheta;

            to.x -= alpha * ex;
            to.y -= alpha * ey;
            to.theta -= alpha * et;
            while (to.theta > M_PI) to.theta -= 2.0f * M_PI;
            while (to.theta < -M_PI) to.theta += 2.0f * M_PI;

            from.x += alpha * ex;
            from.y += alpha * ey;
            from.theta += alpha * et;
            while (from.theta > M_PI) from.theta -= 2.0f * M_PI;
            while (from.theta < -M_PI) from.theta += 2.0f * M_PI;
        }
    }
}

} // namespace aimee_nav_core
