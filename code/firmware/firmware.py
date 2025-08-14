from robot import *
from instruments.rx_comms import * 
from instruments.servo_utility import *

running = True


print("Hello User!")

try:
    pca_obj = PCA9865(0x41, False)
    print("Creating Robot Object...")
    robot = Robot(pca_obj)
    robot.set_all_angles([90,90,90,90,90,90,90,90,90,90,90,90])
    print("Creating Comms Object...")
    rx_comms = RX_Comms()
    
except Exception as e:
    print(e)

#while running:
    # TODO Add stuff here 
    #robot.update()
    #rx_comms.update()
