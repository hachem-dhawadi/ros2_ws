#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

class HelloWorldNode(Node):
    def __init__(self):
        super().__init__('hello_world_node')
        self.counter_ = 0
        # create a timer to call self.call_back every 1 second
        self.timer = self.create_timer(1.0, self.call_back)
    
    def call_back(self):
        self.get_logger().info('Hello World '+str(self.counter_))
        self.counter_ += 1

def main(args=None):
    rclpy.init(args=args)
    node = HelloWorldNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
