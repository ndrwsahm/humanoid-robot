"""arm_tutorial controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = 64

# Left Hip Rotator
lhrm = robot.getDevice('ll1_motor')

lhrps = robot.getDevice('ll1_pos')
lhrps.enable(timestep)

lhrm.setPosition(0.0)
lhrm.setVelocity(1.0)

# Left Hip Abductor
lham = robot.getDevice('ll2_motor')

lhaps = robot.getDevice('ll2_pos')
lhaps.enable(timestep)

lham.setPosition(0.0)
lham.setVelocity(1.0)

# Left Leg 3
lhem = robot.getDevice('ll3_motor')

lheps = robot.getDevice('ll3_pos')
lheps.enable(timestep)

lhem.setPosition(0.0)
lhem.setVelocity(1.0)

# Left Knee
lkkm = robot.getDevice('ll4_motor')

lkkps = robot.getDevice('ll4_pos')
lkkps.enable(timestep)

lkkm.setPosition(1.25)
lkkm.setVelocity(1.0)

# Left Ankle Extender
laem = robot.getDevice('ll5_motor')

laeps = robot.getDevice('ll5_pos')
laeps.enable(timestep)

laem.setPosition(0.0)
laem.setVelocity(1.0)

# Left Ankle Abductor
laam = robot.getDevice('ll6_motor')

laaps = robot.getDevice('ll6_pos')
laaps.enable(timestep)

laam.setPosition(0.0)
laam.setVelocity(1.0)

# Right Hip Rotator
rhrm = robot.getDevice('rl1_motor')

rhrps = robot.getDevice('rl1_pos')
rhrps.enable(timestep)

rhrm.setPosition(0.0)
rhrm.setVelocity(1.0)

# Right Hip Abductor
rham = robot.getDevice('rl2_motor')

rhaps = robot.getDevice('rl2_pos')
rhaps.enable(timestep)

rham.setPosition(0.0)
rham.setVelocity(1.0)

# Right Hip Extender
rhem = robot.getDevice('rl3_motor')

rheps = robot.getDevice('rl3_pos')
rheps.enable(timestep)

rhem.setPosition(0.0)
rhem.setVelocity(1.0)

# Right Knee
rkkm = robot.getDevice('rl4_motor')

rkkps = robot.getDevice('rl4_pos')
rkkps.enable(timestep)

rkkm.setPosition(1.25)
rkkm.setVelocity(1.0)

# Right Ankle Extender
raem = robot.getDevice('rl5_motor')

raeps = robot.getDevice('rl5_pos')
raeps.enable(timestep)

raem.setPosition(0.0)
raem.setVelocity(1.0)

# Right Ankle Abductor
raam = robot.getDevice('rl6_motor')

raaps = robot.getDevice('rl6_pos')
raaps.enable(timestep)
