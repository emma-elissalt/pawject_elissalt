import rclpy
import time
from rclpy.node import Node
from std_msgs.msg import String
import dynamixel_sdk as sdk
from geometry_msgs.msg import Point
from random import randint
class Control(Node):
    def __init__(self):
        super().__init__('control')
        self.subscription = self.create_subscription(String,'/serial_data',self.listener_callback,10)
        self.subscription  # prevent unused variable warning

        # Setup Dynamixel SDK
        self.portHandler = sdk.PortHandler('/dev/ttyACM0')
        self.packetHandler = sdk.PacketHandler(1.0)
        self.DXL_ID = 0  # Dynamixel ID : 1
        self.DXL_ID_2 = 1  # Dynamixel ID : 1

        # Open port
        if not self.portHandler.openPort():
            self.get_logger().error("Failed to open the port")
            exit()

        # Set baudrate
        if not self.portHandler.setBaudRate(1000000):
            self.get_logger().error("Failed to change the baudrate")
            exit()

        self.ADDR_MX_GOAL_POSITION = 30 
        self.ADDR_MX_SPEED = 32
       

    def listener_callback(self, msg):
        self.get_logger().info('Received delivery command: "%s"' % msg.data)
        # Activate servomotor movement here
        self.POSITION_VALUE = 500
        self.move_servo(self.POSITION_VALUE,self.DXL_ID,self.ADDR_MX_SPEED)
        time.sleep(1.5)
        self.move_servo(0,self.DXL_ID,self.ADDR_MX_SPEED)
        time.sleep(2)
        self.move_servo(600,self.DXL_ID_2,self.ADDR_MX_GOAL_POSITION)
        time.sleep(1.5)
        self.move_servo(400,self.DXL_ID_2,self.ADDR_MX_GOAL_POSITION)
            
    def move_servo(self, position, ID, adresse):
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, ID, adresse, position)
        # dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, self.DXL_ID_2, self.ADDR_MX_GOAL_POSITION, position)

        print('lE MOTEUR TOURNE')
        if dxl_comm_result != sdk.COMM_SUCCESS:
            self.get_logger().error(self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            self.get_logger().error(self.packetHandler.getRxPacketError(dxl_error))

        # You might want to read the position back, or add more logic here

    def __del__(self):
        # Close port
        self.portHandler.closePort()


def main(args=None):
    rclpy.init(args=args)
    control= Control()

    try:
        rclpy.spin(control)
    except KeyboardInterrupt:
        print('Servo controller node stopped cleanly')
    except BaseException:
        print('Exception in servo controller:', file=sys.stderr)
        raise
    finally:
        control.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
