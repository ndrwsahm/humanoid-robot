try:
    print("Ignore the error commands starting from here if running without ssh")
    from _firmware.utility_functions import leg
    from _firmware.utility_functions import head
    from _firmware.firmware_globals import *
    from _firmware.utility_functions.settings_parser import load_robot_settings
    from _firmware.utility_functions.username_id import get_robot_id_from_username
    #from _firmware.instruments.accelerometer import MPU6050

except:
    print("Do not ignore the error commands past this point if running with ssh")
    from utility_functions import leg
    from utility_functions import head
    from firmware_globals import *
    from instruments.accelerometer import MPU6050
    from instruments.servo_utility import PCA9865
    from utility_functions.settings_parser import load_robot_settings
    from utility_functions.username_id import get_robot_id_from_username

import time

class Robot:
    def __init__(self, is_recal):
        self.lower_pca = PCA9865(0x41, False)
        self.upper_pca = PCA9865(0x40, False)
        self.is_recal = is_recal    # Recalibrate servo flag

        self.setpoint = 90.0
        self.camera_kp = 20.0
        self.camera_ki = 0.00
        self.camera_kd = 10.0
        self.integral = 0.0

        self.roll = 0.0
        self.pitch = 0.0
        self.yaw = 0.0

        self.last_roll = 0.0
        self.last_time = 0.0
        self.last_error = 0.0

        self.is_walking = False
        self.is_standing = True
        self.is_steady_camera = False

        self.new()

    def new(self):
        robot_id = get_robot_id_from_username()

        if not robot_id:
            print("Could not determine robot ID from username. Running simulated leg ")
            robot_id = "simulate"

        settings = load_robot_settings(robot_id)
        
        print('Building Legs...')
        self.left_leg = leg.Leg(self.lower_pca, "left", settings, self.is_recal)
        self.right_leg = leg.Leg(self.lower_pca, "right", settings, self.is_recal)

        self.head = head.Head(self.upper_pca, settings, self.is_recal)

        self.left_thetas = self.left_leg.get_leg_thetas()
        self.right_thetas = self.right_leg.get_leg_thetas()
        self.head_thetas = self.head.get_head_thetas()
        self.all_thetas = self.left_thetas + self.right_thetas + [90 ,90, 90] + [90, 90, 90] + self.head_thetas
        self.set_all_angles(self.all_thetas)

        self.imu = MPU6050(0x68)
    
    def update(self):
        self.left_leg.update()
        self.right_leg.update()
            
        #self.head.set_head_theta(self.roll, 90)

    # Getters
    ##################################
    def get_accel_data(self):
        self.imu.get_data()
        self.roll, self.pitch, self.yaw = self.imu.get_roll_pitch_yaw()
        self.accel_roll, self.accel_pitch, self.accel_yaw = self.imu.get_accel_roll_pitch_yaw()

        return self.roll, self.pitch, self.yaw, self.accel_roll, self.accel_pitch, self.accel_yaw
    
    def get_all_angles(self):
        return self.all_thetas
    
    def get_pulse_width_settings(self):
        return self.left_leg.get_pulse_widths() + self.right_leg.get_pulse_widths()
    
    # Setters
    ##################################
    def set_all_angles(self, angles):
        self.left_leg.set_leg_theta(angles[0], angles[1], angles[2], angles[3], angles[4], angles[5])  # starting 90 degree position
        self.right_leg.set_leg_theta(angles[6], angles[7], angles[8], angles[9], angles[10], angles[11])  # starting 90 degree position
        #self.left_arm.set_arm_theta(angles[12], angles[13], angles[14])
        #self.right_arm.set_arm_theta(angles[15], angles[16], angles[17])
        if not self.is_steady_camera:
            self.head.set_head_theta(angles[18], angles[19])
        self.all_thetas = angles

    def set_head_angles(self, roll, yaw):
        self.head.set_head_theta(yaw, roll)

    def set_steady_camera(self, bool):
        self.is_steady_camera = bool

    def set_pwm_settings(self, servo, pwm_min, pwm_max):
        if servo < 6:
            self.left_leg.set_servo_pwm_settings(servo, pwm_min, pwm_max)
        else:
            self.right_leg.set_servo_pwm_settings(servo-6, pwm_min, pwm_max)

    # Functions
    ##################################
    def run_steady_camera(self):
        roll, pitch, yaw, accel_roll, accel_pitch, accel_yaw = self.get_accel_data()  # Update IMU data and adjust head position accordingly
        if self.last_roll != roll:

            # Proportional
            error = roll - self.setpoint
            if abs(error) < 10:
                return 
        
            # Clamp outputs
            print(f"IMU Roll: {roll:.2f}, Pitch: {pitch:.2f}, Yaw: {yaw:.2f}")
            self.set_head_angles(roll, 90)  # Example: Set head roll based on IMU data, keep yaw fixed at 90
            self.last_roll = roll

    def smooth_transition_position(self, last_angles, end_angles):
        new_angles = last_angles
        final_true_angles = end_angles.copy()
        fail_list = [1,1,1,1,1,1,1,1,1,1,1,1]

        X = 0.75

        for k in range(len(end_angles)):
            end_angles[k] *= (1-X)

        running = True
        while running:
            for j in range(len(last_angles)):
                last_angles[j] *= X

                new_angles[j] = end_angles[j] + last_angles[j]
                new_angles_rounded = [round(num, 2) for num in new_angles]

                # If difference is less than 1 degree
                if abs(final_true_angles[j] - new_angles[j]) < 1:
                    fail_list[j] = 0
                #print("End Angle" + str(final_true_angles[j]) + " -  New Angle " + str(new_angles[j]) + " = " + str(final_true_angles[j] - new_angles[j]))
            #print("Fail List:   " + str(fail_list))
            if all(item == 0 for item in fail_list):
                running = False
                
            #print("New Angles:    " + str(new_angles_rounded))
            self.set_all_angles(new_angles_rounded)
            last_angles = new_angles_rounded

            #time.sleep(0.05) 