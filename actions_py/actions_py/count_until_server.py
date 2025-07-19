#!/usr/bin/env python3

import rclpy
import time
from rclpy.node import Node
from rclpy.action import ActionServer
from rclpy.action.server import ServerGoalHandle
from my_robot_interfaces.action import CountUntil

class CountUntilServer(Node):
    def __init__(self):
        super().__init__('count_until_server')
        self.count_until_action_server = ActionServer(
            self,
            CountUntil,
            "count_until",
            execute_callback=self.execute_callback
        )
        self.get_logger().info('CountUntil action server has been started.')
    
    def execute_callback(self, goal_handle : ServerGoalHandle):
        target_number = goal_handle.request.target_number
        period = goal_handle.request.period
        self.get_logger().info('excuting goal')
        counter=0
        for i in range  (target_number):
            counter += 1
            self.get_logger().info(f'Current count: {counter}')
            time.sleep(period)

        goal_handle.succeed()
        result = CountUntil.Result()
        result.reached_number = counter
        self.get_logger().info(f'Goal reached: {counter}')
        return result


def main(args=None):
    rclpy.init(args=args)
    node = CountUntilServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
