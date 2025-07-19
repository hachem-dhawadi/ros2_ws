#!/usr/bin/env python3

import rclpy
import time
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.action.client import ClientGoalHandle
from my_robot_interfaces.action import CountUntil

class CountUntilClient(Node):
    def __init__(self):
        super().__init__('count_until_client')
        self.count_until_client = ActionClient(
            self,
            CountUntil,
            "count_until"
        )
        self.get_logger().info('CountUntil action server has been started.')
    
    def send_goal(self, target_number, period):
        self.count_until_client.wait_for_server()

        goal = CountUntil.Goal()
        goal.target_number = target_number
        goal.period = period 
        self.get_logger().info(f'Sending goal: target_number={target_number}, period={period}')
        self.count_until_client.send_goal_async(goal).add_done_callback(self.goal_response_callback)
    
    def goal_response_callback(self, future):
        self.goal_handle: ClientGoalHandle = future.result()
        if self.goal_handle.accepted:
            self.get_logger().info('Goal accepted by server, waiting for result...')
            self.goal_handle.get_result_async().add_done_callback(self.goal_result_callback)
    
    def goal_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Goal completed with result: {result.reached_number}')



def main(args=None):
    rclpy.init(args=args)
    node = CountUntilClient()
    node.send_goal(10, 1)  # Example call to send a goal
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
