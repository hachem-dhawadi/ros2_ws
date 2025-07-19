#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from  turtlesim.msg import Pose

class PoseSubscriberNode(Node):
    def __init__(self):
        super().__init__('pose_subscriber_node')
        self.pose_subscriber_node = self.create_subscription(Pose, "/turtle1/pose", self.pose_callback, 10)

    def pose_callback(self,msg:Pose):
        self.get_logger().info(str(msg))
        # call this function again after

def main(args=None):
    rclpy.init(args=args)
    node = PoseSubscriberNode() 
    rclpy.spin(node)
    #node.destroy_node()
    rclpy.shutdown()

#if you want to run th script directly from the terminal
if __name__ == '__main__':
    main()
