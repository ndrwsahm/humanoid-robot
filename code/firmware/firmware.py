from robot import *
from instruments.rx_comms import * 
from instruments.servo_utility import *

running = True


print("Hello User!")

try:
    pca_obj = PCA9865(0x40, False)
    print("Creating Robot Object...")
    robot = Robot(pca_obj)

    print("Creating Comms Object...")
    rx_comms = RX_Comms()
    
except Exception as e:
    print(e)

    #while running:
    #    robot.update()
    #    rx_comms.update()
