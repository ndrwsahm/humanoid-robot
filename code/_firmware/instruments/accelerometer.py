from mpu6050 import mpu6050

DEBUG_PRINT_STATEMENT = True
PRINT_ITERATIONS = 50

class MPU6050:
    def __init__(self, addr):
        self.sensor = mpu6050(addr)
        self.counter = 0

    def get_data(self):
        accel_data = self.sensor.get_accel_data()
        gyro_data = self.sensor.get_gyro_data()

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

if __name__ == "__main__":
    acc = MPU6050(0x68)
    while True:
        acc.get_data()
