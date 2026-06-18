import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, PoseStamped
from nav_msgs.msg import Odometry, OccupancyGrid
import math

class NavNode(Node):
    def __init__(self):
        super().__init__('nav_node')
        self.subscription = self.create_subscription(
            PoseStamped,
            '/goal_pose',
            self.goal_callback,
            10)
        self.odom_sub = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10)
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.current_pose = None
        self.goal_pose = None
        self.timer = self.create_timer(0.1, self.timer_callback)

    def odom_callback(self, msg):
        self.current_pose = msg.pose.pose

    def goal_callback(self, msg):
        self.goal_pose = msg.pose
        self.get_logger().info('New goal received')

    def timer_callback(self):
        if self.current_pose is None or self.goal_pose is None:
            return

        dx = self.goal_pose.position.x - self.current_pose.position.x
        dy = self.goal_pose.position.y - self.current_pose.position.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance < 0.1:
            self.get_logger().info('Goal reached!')
            self.goal_pose = None
            self.publisher_.publish(Twist())
            return

        angle_to_goal = math.atan2(dy, dx)
        
        # Simple proportional control
        msg = Twist()
        # Linear velocity proportional to distance, capped at 0.2 m/s
        msg.linear.x = min(0.2, distance)
        
        # Note: In a real implementation, you'd also want to rotate towards the goal.
        # This simple version just moves forward in the current orientation's 'x' direction.
        
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = NavNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
