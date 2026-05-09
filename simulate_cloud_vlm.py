#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from aimee_msgs.msg import CloudIntent
import json
import time

class CloudSimulator(Node):
    def __init__(self):
        super().__init__('cloud_simulator')
        self.pub = self.create_publisher(CloudIntent, '/cloud/game_move', 10)
        
    def send_pick_command(self, obj_class, color):
        msg = CloudIntent()
        # We repurposed game_move to handle generic commands from the cloud bridge
        # The bridge expects JSON in move_json.
        cmd = {
            "type": "skill",
            "name": "pick_place",
            "parameters": {
                "object_class": obj_class,
                "color": color,
                "enable_place": True
            }
        }
        msg.move_json = json.dumps(cmd)
        
        print(f"Sending VLM simulation command: Pick up the {color} {obj_class}")
        self.pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = CloudSimulator()
    time.sleep(1.0) # Wait for connections
    node.send_pick_command("block", "red")
    time.sleep(1.0)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
