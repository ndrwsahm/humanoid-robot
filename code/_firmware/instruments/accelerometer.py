import math
import time
from mpu6050 import mpu6050

DEBUG_PRINT_STATEMENT = False
PRINT_ITERATIONS = 50

class MPU6050:
    def __init__(self, addr):
        self.sensor = mpu6050(addr)
        self.counter = 0

        self.last_time = time.time()
        # Initialize angles
        self.roll = 0.0
        self.pitch = 0.0
        self.yaw = 0.0

        self.accel_yaw = 0.0
        self.accel_pitch = 0.0
        self.accel_roll = 0.0

        self.last_data = [0.0, 0.0, 0.0]

    def get_data(self):
        accel_data = self.sensor.get_accel_data()
        gyro_data = self.sensor.get_gyro_data()

        # Update relative angle
        self.update_angle(accel_data, gyro_data)

        if DEBUG_PRINT_STATEMENT:
            self.counter += 1
            if self.counter % PRINT_ITERATIONS == 0:  # only print every 20th call
                self.print_data(accel_data, gyro_data)

        else:
            self.return_data(accel_data, gyro_data)

    def print_data(self, accel_data, gyro_data):
        print("\n=== MPU6050 Sensor Data ===")
        print(f"{'Sensor':<15} | {'X':>10} | {'Y':>10} | {'Z':>10}")
        print("-" * 50)
        print(f"{'Accelerometer':<15} | {accel_data['x']:>10.2f} | {accel_data['y']:>10.2f} | {accel_data['z']:>10.2f}")
        print(f"{'Gyroscope':<15} | {gyro_data['x']:>10.2f} | {gyro_data['y']:>10.2f} | {gyro_data['z']:>10.2f}")
        print("=" * 50)
        print(f"Roll: {self.roll:.2f}°, Pitch: {self.pitch:.2f}°, Yaw: {self.yaw:.2f}°")

    def return_data(self, accel_data, gyro_data):
        print(f"IMU: {self.roll:.2f}, {self.pitch:.2f}, {self.yaw:.2f}, {accel_data['x']:.2f}, {accel_data['y']:.2f}, {accel_data['z']:.2f}, {gyro_data['x']:.2f}, {gyro_data['y']:.2f}, {gyro_data['z']:.2f}")

    def update_angle(self, accel_data, gyro_data):
        # Time delta
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time

        # Gyro rates (deg/s)
        gyro_x = gyro_data['x']
        gyro_y = gyro_data['y']
        gyro_z = gyro_data['z']

        # Integrate gyro to estimate angle
        self.yaw += gyro_x * dt
        self.pitch += gyro_y * dt
        self.roll += gyro_z * dt  # Yaw can be tracked but is less reliable without a magnetometer

        # Accelerometer angle (in degrees)
        self.accel_yaw = math.degrees(math.atan2(accel_data['y'], accel_data['z']))
        self.accel_pitch = math.degrees(math.atan2(-accel_data['y'], accel_data['x']))
        self.accel_roll = math.degrees(math.atan2(accel_data['z'], accel_data['x']))

        # Low Pass filter (fusion of gyro + accel)
        alpha = 0.35 # weight for gyro
        self.roll = alpha * self.roll + (1 - alpha) * self.accel_roll
        self.pitch = (alpha * self.pitch + (1 - alpha) * self.accel_pitch)
        self.yaw = alpha * self.yaw + (1 - alpha) * self.accel_yaw

        self.roll += 90

    def apply_lowpass_filter(self, raw_data):
        alpha = 0.15
        filtered_data = []
        for k in range(len(raw_data)):
            filtered_data[k] = alpha*raw_data[k] + (1.0 - alpha)*self.last_data[k]
            self.last_data[k] = filtered_data[k]
        return filtered_data

    def get_roll_pitch_yaw(self):
        return self.roll, self.pitch, self.yaw

    def get_accel_roll_pitch_yaw(self):
        return self.accel_roll, self.accel_pitch, self.accel_yaw
    
if __name__ == "__main__":
    acc = MPU6050(0x68)
    DEBUG_PRINT_STATEMENT = False
    while True:
        acc.get_data()
        #time.sleep(0.05)  # 20 Hz sampling
