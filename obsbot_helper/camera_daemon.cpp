// Camera keep-alive daemon
#include <iostream>
#include <thread>
#include <chrono>
#include <atomic>
#include <csignal>
#include "dev/devs.hpp"

std::atomic<bool> g_running(true);
std::shared_ptr<Device> g_device = nullptr;

void signal_handler(int sig) {
    g_running = false;
}

int main() {
    std::signal(SIGINT, signal_handler);
    std::signal(SIGTERM, signal_handler);
    
    std::cout << "Camera daemon starting..." << std::endl;
    
    Devices& devices = Devices::get();
    
    // Wait for device
    std::cout << "Waiting for camera..." << std::endl;
    for (int i = 0; i < 50 && g_running; i++) {
        auto devList = devices.getDevList();
        if (!devList.empty()) {
            g_device = devList.front();
            std::cout << "Camera connected: " << g_device->devSn() << std::endl;
            break;
        }
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
    
    if (!g_device) {
        std::cerr << "Camera not found" << std::endl;
        return 1;
    }
    
    // Wake up camera
    g_device->cameraSetDevRunStatusR(Device::DevStatusRun);
    std::cout << "Camera awake" << std::endl;
    
    // Keep-alive loop
    std::cout << "Keep-alive running (Ctrl+C to stop)..." << std::endl;
    while (g_running) {
        // Small movement to keep awake
        g_device->aiSetGimbalSpeedCtrlR(0.5, 0, 0);
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
        g_device->aiSetGimbalSpeedCtrlR(-0.5, 0, 0);
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
        g_device->aiSetGimbalStop();
        
        // Wait before next keep-alive
        std::this_thread::sleep_for(std::chrono::seconds(5));
    }
    
    std::cout << "Shutting down..." << std::endl;
    return 0;
}
