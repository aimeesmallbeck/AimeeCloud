#pragma once

#include <vector>
#include <tuple>
#include <cstdint>

namespace aimee_nav_core {

/**
 * @brief Simple 2D pose graph for loop closure.
 *
 * Stores keyframes (pose + scan points). Adds constraints
 * between nearby keyframes and runs Gauss-Newton relaxation.
 */
struct Keyframe {
    float x = 0.0f, y = 0.0f, theta = 0.0f;
    std::vector<float> xs; // scan hit points in map frame
    std::vector<float> ys;
};

struct Constraint {
    int from = 0;
    int to = 0;
    float dx = 0.0f;
    float dy = 0.0f;
    float dtheta = 0.0f;
};

class PoseGraph {
public:
    PoseGraph() = default;

    /** Add a new keyframe. Returns its index. */
    int add_keyframe(const Keyframe& kf);

    /** Find nearby keyframe indices within radius_m of (x,y). */
    std::vector<int> find_nearby(float x, float y, float radius_m) const;

    /** Add a loop-closure constraint between two keyframes. */
    void add_constraint(int from, int to, float dx, float dy, float dtheta);

    /** Run Gauss-Newton relaxation (async-friendly; small number of iterations). */
    void optimize(int iterations = 10);

    const std::vector<Keyframe>& keyframes() const { return keyframes_; }
    std::vector<Keyframe>& keyframes() { return keyframes_; }

    const std::vector<Constraint>& constraints() const { return constraints_; }
    std::vector<Constraint>& constraints() { return constraints_; }

private:
    std::vector<Keyframe> keyframes_;
    std::vector<Constraint> constraints_;
};

} // namespace aimee_nav_core
