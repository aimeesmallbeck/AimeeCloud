// Simple OBSBOT control helper
// Compiles against libdev.so

#include <iostream>
#include <cstring>
#include <unistd.h>
#include <sstream>
#include <vector>
#include <sys/socket.h>
#include <sys/un.h>
#include <signal.h>
#include "dev/devs.hpp"

std::shared_ptr<Device> g_device = nullptr;
bool g_device_found = false;

void waitForDevice(Devices& devices, int timeout_ms = 5000) {
    int waited = 0;
    while (waited < timeout_ms) {
        auto devList = devices.getDevList();
        if (!devList.empty()) {
            g_device = devList.front();
            g_device_found = true;
            return;
        }
        usleep(100000);
        waited += 100;
    }
}

int executeCommand(const std::vector<std::string>& args) {
    if (!g_device_found || !g_device) return 1;
    if (args.empty()) return 1;
    const std::string& cmd = args[0];
    if (cmd == "list") {
        return 0;
    } else if (cmd == "gimbal" && args.size() >= 4) {
        double yaw = std::stod(args[1]);
        double pitch = std::stod(args[2]);
        double roll = std::stod(args[3]);
        return g_device->aiSetGimbalSpeedCtrlR(yaw, pitch, roll);
    } else if (cmd == "zoom" && args.size() >= 2) {
        float zoom = std::stof(args[1]);
        return g_device->cameraSetZoomAbsoluteR(zoom, 6);
    } else if (cmd == "aimode" && args.size() >= 3) {
        int mode = std::stoi(args[1]);
        int sub = std::stoi(args[2]);
        return g_device->cameraSetAiModeU((Device::AiWorkModeType)mode, sub);
    } else if (cmd == "sleep") {
        return g_device->cameraSetDevRunStatusR(Device::DevStatusSleep);
    } else if (cmd == "wakeup") {
        return g_device->cameraSetDevRunStatusR(Device::DevStatusRun);
    } else if (cmd == "stop") {
        return g_device->aiSetGimbalStop();
    }
    return 1;
}

int runDaemon(const char* socket_path) {
    signal(SIGPIPE, SIG_IGN);
    Devices& devices = Devices::get();
    waitForDevice(devices);
    if (!g_device_found) {
        std::cerr << "No device found" << std::endl;
        return 1;
    }

    int fd = socket(AF_UNIX, SOCK_STREAM, 0);
    if (fd < 0) {
        perror("socket");
        return 1;
    }

    unlink(socket_path);
    struct sockaddr_un addr;
    memset(&addr, 0, sizeof(addr));
    addr.sun_family = AF_UNIX;
    strncpy(addr.sun_path, socket_path, sizeof(addr.sun_path)-1);

    if (bind(fd, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
        perror("bind");
        return 1;
    }

    if (listen(fd, 5) < 0) {
        perror("listen");
        return 1;
    }

    while (true) {
        int client = accept(fd, nullptr, nullptr);
        if (client < 0) continue;

        char buf[256];
        ssize_t n = read(client, buf, sizeof(buf)-1);
        if (n > 0) {
            buf[n] = '\0';
            std::string line(buf);
            size_t end = line.find_last_not_of("\r\n");
            if (end != std::string::npos) line = line.substr(0, end+1);

            std::istringstream iss(line);
            std::vector<std::string> args;
            std::string arg;
            while (iss >> arg) args.push_back(arg);

            int ret = 1;
            try {
                ret = executeCommand(args);
            } catch (...) {
                ret = 1;
            }
            std::string response = (ret == 0) ? "OK\n" : "ERR\n";
            write(client, response.c_str(), response.size());
        }
        close(client);
    }
    return 0;
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
        std::cerr << "  daemon <socket>   - Run as daemon over unix socket" << std::endl;
        return 1;
    }

    std::string cmd = argv[1];
    if (cmd == "daemon" && argc >= 3) {
        return runDaemon(argv[2]);
    }

    Devices& devices = Devices::get();
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

    std::vector<std::string> args;
    for (int i = 1; i < argc; ++i) args.push_back(argv[i]);
    return executeCommand(args);
}
