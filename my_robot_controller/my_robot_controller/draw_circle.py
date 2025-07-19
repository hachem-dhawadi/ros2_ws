#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class DrawCircle(Node):
    def __init__(self):
        super().__init__('draw_circle_node')
        self.cmd_vel_pub_ = self.create_publisher(Twist,"/turtle1/cmd_vel", 10)
        self.timer = self.create_timer(0.5, self.call_back_send_velocity)
        self.get_logger().info('draw circle node has been started')

    def call_back_send_velocity(self):
        msg = Twist()
        msg.linear.x = 2.0
        msg.angular.z = 1.0
        self.cmd_vel_pub_.publish(msg)
        self.get_logger().info('Publishing: linear.x = %f, angular.z = %f' % (msg.linear.x, msg.angular.z))
        # call this function again after

def main(args=None):
    rclpy.init(args=args)
    node = DrawCircle() 
    rclpy.spin(node)
    #node.destroy_node()
    rclpy.shutdown()

#if you want to run th script directly from the terminal
if __name__ == '__main__':
    main()
