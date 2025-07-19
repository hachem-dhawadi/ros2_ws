#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from  turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from functools import partial
from turtlesim.srv import SetPen

class TurtleController(Node):
    def __init__(self):
        self.previous_x = 0
        super().__init__('turtle_controller_node')
        self.get_logger().info("a Turtle Controller Node has been started")
        self.cmd_vel_pub_ = self.create_publisher(Twist,"/turtle1/cmd_vel", 10)
        self.pose_subscriber_node = self.create_subscription(Pose, "/turtle1/pose", self.pose_callback, 10)

    def pose_callback(self,pose:Pose):
        cmd = Twist()
        if pose.x > 9.0 or pose.x < 2.0 or pose.y > 9.0 or pose.y < 2.0:
            cmd.linear.x = 1.0
            cmd.angular.z = 0.9
            self.get_logger().info('Turtle is at position: x = %f, y = %f' % (pose.x, pose.y))
            #self.send_velocity_command()
        else:
            cmd.linear.x = 5.0
            cmd.angular.z = 0.0
            self.get_logger().info('Turtle is at position: x = %f, y = %f' % (pose.x, pose.y))
        self.cmd_vel_pub_.publish(cmd)

        if pose.x > 5.5 and self.previous_x <= 5.5:
            self.get_logger().info('Turtle is in the red zone')
            self.previous_x = pose.x
            self.call_set_pen_service(255, 0, 0, 3, 0)

        elif pose.x < 5.5 and self.previous_x >= 5.5:
            self.get_logger().info('Turtle is in the green zone')
            self.previous_x = pose.x
            self.call_set_pen_service(0, 255, 0, 3, 0)
            #self.send_velocity_command()
    
    def call_set_pen_service(self, r, g, b, width, off):
        client = self.create_client(SetPen, '/turtle1/set_pen')
        while not client.wait_for_service(1.0):
            self.get_logger().warn('Service not available, waiting again...')
        request = SetPen.Request()
        request.r = r
        request.g = g
        request.b = b
        request.width = width
        request.off = off
        future = client.call_async(request)
        future.add_done_callback(partial(self.call_back_set_pen))
        #rclpy.spin_until_future_complete(self, future)
        #return future.result()
    
    def call_back_set_pen(self, future):
        try:
            response = future.result()
        except Exception as e:
            self.get_logger().error('Service call failed: %r' % (e,))

def main(args=None):
    rclpy.init(args=args)
    node = TurtleController() 
    rclpy.spin(node)
    #node.destroy_node()
    rclpy.shutdown()

#if you want to run th script directly from the terminal
if __name__ == '__main__':
    main()
