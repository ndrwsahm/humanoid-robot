import time

MIN_DEGREES_PER_ROT = 1
MIN_TIME_PER_ROT = 0.05 # Lowest value acceptable is 0.05

class PCA9865:
    def __init__(self, addr, simulate):
        self.simulate = simulate

        if not self.simulate:
            from adafruit_servokit import ServoKit

            #Initialize the PCA9685 with default address (0x40)
            self.pca = ServoKit(channels=16, address=addr)
        else:
            print("Simulating PCA Object")

        self.min_step_size = MIN_DEGREES_PER_ROT

    def set_pulse_min_max(self, servo_num, pulse_min, pulse_max):
        if not self.simulate:
            self.pca.servo[servo_num].set_pulse_width_range(pulse_min, pulse_max)
        else:
            print("Virtual Servo " + str(servo_num) + "     Min : " + str(pulse_min) + "     Max : " + str(pulse_max))

    def set_servo_angle(self, servo_num, angle):
        if not self.simulate:
            self.pca.serv[servo_num].angle = angle
        else:
            print("Virtual Servo " + str(servo_num) + "     Set to : " + str(angle))

    def sweep_servo_time(self, servo_num, from_angle, to_angle, total_time):
        elapsed_time = 0
        angle = from_angle
        if not self.simulate:
            self.pca.servo[servo_num].angle = angle
        
        velocity = (to_angle - from_angle) / total_time 
        step_size = velocity * MIN_TIME_PER_ROT

        while angle < to_angle:
            angle += step_size 
            elapsed_time += MIN_TIME_PER_ROT
            if not self.simulate:
                self.pca.servo[servo_num].angle = angle
            else:
                print("Virtual Servo " + str(servo_num) + "     Set to: " + str(angle) + "  at time: " + str(elapsed_time))    
            time.sleep(MIN_TIME_PER_ROT)
    
    def calibrate_servo(self, servo_num):
        acceptable_responses = ["y", "n+", "n-"]

        print("Calibrating...")
        self.set_servo_angle(servo_num, 0)

        self.sweep_servo_time(servo_num, 0, 180, 3)

        user_response = "new"
        while user_response != "y":
            print("Did the servo make transition from 0 deg to 180 deg? y/n+/n-")
            user_response = input()
            if user_response in acceptable_responses:
                pass
            else:
                print("Not a valid selection") 

        self.set_servo_angle(servo_num, 90)
        print("Calibration Complete!!! Servo " + str(servo_num) + " set to 90 deg")

