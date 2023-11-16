import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial


class SerialPort(Node):
    def __init__(self):
        super().__init__('serialport')
        self.publisher = self.create_publisher(String,'serial_data',10)
        self.serial_port = "/dev/ttyUSB0"
        self.baudrate = 115200
        self.timeout = 1     
        self.read_serial()
        
    def read_serial(self):       
        # try:
        ser = serial.Serial(self.serial_port, self.baudrate, timeout=self.timeout)
        self.get_logger().info(f"Serial port {self.serial_port} opened successfully.")

        while rclpy.ok():
            # Read data from the serial port
            data = ser.readline().decode('utf-8').strip()

            # Publish the received data to the ROS 2 topic
            if data:
                msg = String()
                msg.data = data
                self.publisher.publish(msg)
                self.get_logger().info(f"Published: {data}")

        # except serial.SerialException as e:
        #     self.get_logger().error(f"Error: {e}")
        # finally:
        #     if ser.is_open:
        #         ser.close()
        #         self.get_logger().info("Serial port closed.")

        

def main(args=None):
    rclpy.init(args=args)


    serialport = SerialPort()

    try:
        rclpy.spin(serialport)
    except KeyboardInterrupt:
        print('Servo controller node stopped cleanly')
    except BaseException:
        print('Exception in servo controller:', file=sys.stderr)
        raise
    finally:
        serial_port.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
