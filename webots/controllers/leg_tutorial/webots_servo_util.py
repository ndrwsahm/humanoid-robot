TIMESTEP = 64
SPEED = 1

class Servo:
    def __init__(self, motor_name, sensor_name):
        self.motor = robot.getDevice(motor_name)
        
        self.pos_sensor = robot.getDevice(sensor_name)
        self.pos_sensor.enable(TIMESTEP)
        
        self.motor.setPosition(float('inf'))
        self.motor.setVelocity(SPEED)
        
        self.angle_rad = 0.0
        self.angle_deg = 0.0
        
        self.last_angle_rad = 0.0
        self.last_angle_deg = 0.0
        
    def set_position(self, angle):
        if angle > self.last_angle_deg:
            self.motor.setVelocity(SPEED)
        else:
            self.motor.setVelocity(-SPEED)
            
        self.angle_rad = self.pos_sensor.getValue()
        self.angle_deg = 180 / 3.14 * self.angle_rad
        print(self.angle_deg)
        
        if self.angle_deg == angle:
             self.motor.setVelocity(0)   
        
       