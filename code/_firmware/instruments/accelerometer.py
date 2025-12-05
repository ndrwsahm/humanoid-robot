import math
import time
from mpu6050 import mpu6050

DEBUG_PRINT_STATEMENT = True
PRINT_ITERATIONS = 50

class MPU6050:
    def __init__(self, addr):
        self.sensor = mpu6050(addr)
        self.counter = 0

        self.last_time = time.time()
        # Initialize angles
        self.roll = 0.0
        self.pitch = 0.0

    def get_data(self):
        accel_data = self.sensor.get_accel_data()
        gyro_data = self.sensor.get_gyro_data()

        # Update relative angle
        self.update_angle(accel_data, gyro_data)

        if DEBUG_PRINT_STATEMENT:
            self.counter += 1
            if self.counter % PRINT_ITERATIONS == 0:  # only print every 20th call
                self.print_data(accel_data, gyro_data)

    def print_data(self, accel_data, gyro_data):
        print("\n=== MPU6050 Sensor Data ===")
        print(f"{'Sensor':<15} | {'X':>10} | {'Y':>10} | {'Z':>10}")
        print("-" * 50)
        print(f"{'Accelerometer':<15} | {accel_data['x']:>10.2f} | {accel_data['y']:>10.2f} | {accel_data['z']:>10.2f}")
        print(f"{'Gyroscope':<15} | {gyro_data['x']:>10.2f} | {gyro_data['y']:>10.2f} | {gyro_data['z']:>10.2f}")
        print("=" * 50)
        print(f"Roll: {self.roll:.2f}°, Pitch: {self.pitch:.2f}°")

    def update_angle(self, accel_data, gyro_data):
        # Time delta
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time

        # Gyro rates (deg/s)
        gyro_x = gyro_data['x']
        gyro_y = gyro_data['y']

        # Integrate gyro to estimate angle
        self.roll += gyro_x * dt
        self.pitch += gyro_y * dt

        # Accelerometer angle (in degrees)
        accel_roll = math.degrees(math.atan2(accel_data['y'], accel_data['z']))
        accel_pitch = math.degrees(math.atan2(-accel_data['x'], accel_data['y']))

        # Complementary filter (fusion of gyro + accel)
        alpha = 0.0  # weight for gyro
        self.roll = alpha * self.roll + (1 - alpha) * accel_roll
        self.pitch = alpha * self.pitch + (1 - alpha) * accel_pitch

if __name__ == "__main__":
    acc = MPU6050(0x68)
    while True:
        acc.get_data()
        time.sleep(0.05)  # 20 Hz sampling
