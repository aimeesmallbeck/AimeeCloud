// Simple OBSBOT control helper
// Compiles against libdev.so

#include <iostream>
#include <cstring>
#include <unistd.h>
#include "dev/devs.hpp"

// Global device reference
std::shared_ptr<Device> g_device = nullptr;
bool g_device_found = false;

void waitForDevice(Devices& devices, int timeout_ms = 5000) {
    int waited = 0;
    while (waited < timeout_ms) {
        auto devList = devices.getDevList();
        if (!devList.empty()) {
            g_device = devList.front();
            g_device_found = true;
            std::cout << "Device found: " << g_device->devSn() << std::endl;
            return;
        }
        usleep(100000);  // 100ms
        waited += 100;
    }
}

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <command> [args...]" << std::endl;
        std::cerr << "Commands:" << std::endl;
        std::cerr << "  list              - List devices" << std::endl;
        std::cerr << "  gimbal <y> <p> <r> - Set gimbal speed (yaw, pitch, roll)" << std::endl;
        std::cerr << "  zoom <level>      - Set zoom (1.0-4.0)" << std::endl;
        std::cerr << "  aimode <mode> <sub> - Set AI mode" << std::endl;
        std::cerr << "  sleep             - Sleep device" << std::endl;
        std::cerr << "  wakeup            - Wake device" << std::endl;
        std::cerr << "  stop              - Stop gimbal" << std::endl;
        return 1;
    }

    std::string cmd = argv[1];
    
    // Get devices manager
    Devices& devices = Devices::get();
    
    // Wait for device
    waitForDevice(devices);
    
    if (!g_device_found) {
        std::cerr << "No device found within timeout" << std::endl;
        return 1;
    }
    
    if (cmd == "list") {
        std::cout << "Device SN: " << g_device->devSn() << std::endl;
        std::cout << "Device Name: " << g_device->devName() << std::endl;
        std::cout << "Product Type: " << g_device->productType() << std::endl;
        return 0;
    }
    else if (cmd == "gimbal" && argc >= 5) {
        double yaw = std::stod(argv[2]);
        double pitch = std::stod(argv[3]);
        double roll = std::stod(argv[4]);
        int ret = g_device->aiSetGimbalSpeedCtrlR(yaw, pitch, roll);
        std::cout << "Gimbal: " << yaw << ", " << pitch << ", " << roll << " -> " << ret << std::endl;
        return ret;
    }
    else if (cmd == "zoom" && argc >= 3) {
        float zoom = std::stof(argv[2]);
        int ret = g_device->cameraSetZoomAbsoluteR(zoom, 6);
        std::cout << "Zoom: " << zoom << " -> " << ret << std::endl;
        return ret;
    }
    else if (cmd == "aimode" && argc >= 4) {
        int mode = std::stoi(argv[2]);
        int sub = std::stoi(argv[3]);
        int ret = g_device->cameraSetAiModeU((Device::AiWorkModeType)mode, sub);
        std::cout << "AI mode: " << mode << ", " << sub << " -> " << ret << std::endl;
        return ret;
    }
    else if (cmd == "sleep") {
        int ret = g_device->cameraSetDevRunStatusR(Device::DevStatusSleep);
        std::cout << "Sleep -> " << ret << std::endl;
        return ret;
    }
    else if (cmd == "wakeup") {
        int ret = g_device->cameraSetDevRunStatusR(Device::DevStatusRun);
        std::cout << "Wake -> " << ret << std::endl;
        return ret;
    }
    else if (cmd == "stop") {
        int ret = g_device->aiSetGimbalStop();
        std::cout << "Stop -> " << ret << std::endl;
        return ret;
    }
    
    std::cerr << "Unknown command: " << cmd << std::endl;
    return 1;
}
