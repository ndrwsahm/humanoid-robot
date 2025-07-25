"""arm_tutorial controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = 64

rfm = robot.getDevice('rf_motor')
lfm = robot.getDevice('lf_motor')
rbm = robot.getDevice('rb_motor')
lbm = robot.getDevice('lb_motor')

rfps = robot.getPositionSensor('rf_ps')
rfps.enable(timestep)
lfps = robot.getPositionSensor('lf_ps')
lfps.enable(timestep)
rbps = robot.getPositionSensor('rb_ps')
rbps.enable(timestep)
lbps = robot.getPositionSensor('lb_ps')
lbps.enable(timestep)

rfm.setPosition(float('inf'))
rfm.setVelocity(0.0)
lfm.setPosition(float('inf'))
lfm.setVelocity(0.0)
rbm.setPosition(float('inf'))
rbm.setVelocity(0.0)
lbm.setPosition(float('inf'))
lbm.setVelocity(0.0)

rfm2 = robot.getDevice('rf_motor_2')
lfm2 = robot.getDevice('lf_motor_2')
rbm2 = robot.getDevice('rb_motor_2')
lbm2 = robot.getDevice('lb_motor_2')

rfps2 = robot.getPositionSensor('rf_ps_2')
rfps2.enable(timestep)
lfps2 = robot.getPositionSensor('lf_ps_2')
lfps2.enable(timestep)
rbps2 = robot.getPositionSensor('rb_ps_2')
rbps2.enable(timestep)
lbps2 = robot.getPositionSensor('lb_ps_2')
lbps2.enable(timestep)

rfm2.setPosition(float('inf'))
rfm2.setVelocity(0.0)
lfm2.setPosition(float('inf'))
lfm2.setVelocity(0.0)
rbm2.setPosition(float('inf'))
rbm2.setVelocity(0.0)
lbm2.setPosition(float('inf'))
lbm2.setVelocity(0.0)

speed = 1
k = 0

while (robot.step(timestep) != -1):
   
    # Right Front
    #rfm.setVelocity(speed)
    #rfk=rfps.getValue()
    #rfk_deg=180/3.14*rfk
    #print(rfk_deg)
    
    # Left Front
    #lfm.setVelocity(speed)
    #lfk=lfps.getValue()
    #lfk_deg=180/3.14*lfk
    #print(lfk_deg)
    
    # Right Back
    #rbm.setVelocity(speed)
    #rbk=rbps.getValue()
    #rbk_deg=180/3.14*rbk
    #print(rbk_deg)
    
    # Left Back
    #lbm.setVelocity(speed)
    #lbk=lbps.getValue()
    #lbk_deg=180/3.14*lbk
    #print(lbk_deg)
    
    # Right Front 2
    rfm2.setVelocity(speed)
    rfk2=rfps2.getValue()
    rfk2_deg=180/3.14*rfk2
    print(rfk2_deg)
    
    # Left Front 2
    lfm2.setVelocity(speed)
    lfk2=lfps2.getValue()
    lfk2_deg=180/3.14*lfk2
    print(lfk2_deg)
    
    # Right Back 2
    rbm2.setVelocity(speed)
    rbk2=rbps2.getValue()
    rbk2_deg=180/3.14*rbk2
    print(rbk2_deg)
    
    # Left Back 2
    lbm2.setVelocity(speed)
    lbk2=lbps2.getValue()
    lbk2_deg=180/3.14*lbk2
    print(lbk2_deg)
    



