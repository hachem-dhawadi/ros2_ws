from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
import rclpy
from rclpy.node import Node
import time

class TfPublisher(Node):
    def __init__(self):
        super().__init__('tf_broadcaster')
        self.br = TransformBroadcaster(self)
        self.timer = self.create_timer(0.1, self.broadcast_tf)

    def broadcast_tf(self):
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'base_link'
        t.child_frame_id = 'laser_frame'
        t.transform.translation.x = 0.1  # 10cm forward
        t.transform.translation.y = 0.0
        t.transform.translation.z = 0.2  # 20cm high
        t.transform.rotation.w = 1.0  # No rotation
        self.br.sendTransform(t)

rclpy.init()
node = TfPublisher()
rclpy.spin(node)
