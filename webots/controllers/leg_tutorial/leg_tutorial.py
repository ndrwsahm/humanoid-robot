"""arm_tutorial controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = 64

# Left Leg 1
ll1m = robot.getDevice('ll1_motor')

ll1ps = robot.getDevice('ll1_pos')
ll1ps.enable(timestep)

ll1m.setPosition(float('inf'))
ll1m.setVelocity(0.0)

# Left Leg 2
ll2m = robot.getDevice('ll2_motor')

ll2ps = robot.getDevice('ll2_pos')
ll2ps.enable(timestep)

ll2m.setPosition(float('inf'))
ll2m.setVelocity(0.0)

# Left Leg 3
ll3m = robot.getDevice('ll3_motor')

ll3ps = robot.getDevice('ll3_pos')
ll3ps.enable(timestep)

ll3m.setPosition(float('inf'))
ll3m.setVelocity(0.0)

# Left Leg 4
ll4m = robot.getDevice('ll4_motor')

ll4ps = robot.getDevice('ll4_pos')
ll4ps.enable(timestep)

ll4m.setPosition(float('inf'))
ll4m.setVelocity(0.0)

# Left Leg 5
ll5m = robot.getDevice('ll5_motor')

ll5ps = robot.getDevice('ll5_pos')
ll5ps.enable(timestep)

ll5m.setPosition(float('inf'))
ll5m.setVelocity(0.0)

# Left Leg 6
ll6m = robot.getDevice('ll6_motor')

ll6ps = robot.getDevice('ll6_pos')
ll6ps.enable(timestep)

ll6m.setPosition(float('inf'))
ll6m.setVelocity(0.0)

# Left Leg 1
rl1m = robot.getDevice('rl1_motor')

rl1ps = robot.getDevice('rl1_pos')
rl1ps.enable(timestep)

rl1m.setPosition(float('inf'))
rl1m.setVelocity(0.0)

# Right Leg 2
rl2m = robot.getDevice('rl2_motor')

rl2ps = robot.getDevice('rl2_pos')
rl2ps.enable(timestep)

rl2m.setPosition(float('inf'))
rl2m.setVelocity(0.0)

# Right Leg 3
rl3m = robot.getDevice('rl3_motor')

rl3ps = robot.getDevice('rl3_pos')
rl3ps.enable(timestep)

rl3m.setPosition(float('inf'))
rl3m.setVelocity(0.0)

# Right Leg 4
rl4m = robot.getDevice('rl4_motor')

rl4ps = robot.getDevice('rl4_pos')
rl4ps.enable(timestep)

rl4m.setPosition(float('inf'))
rl4m.setVelocity(0.0)

# Right Leg 5
rl5m = robot.getDevice('rl5_motor')

rl5ps = robot.getDevice('rl5_pos')
rl5ps.enable(timestep)

rl5m.setPosition(float('inf'))
rl5m.setVelocity(0.0)

# Right Leg 6
rl6m = robot.getDevice('rl6_motor')

rl6ps = robot.getDevice('rl6_pos')
rl6ps.enable(timestep)

rl6m.setPosition(float('inf'))
rl6m.setVelocity(0.0)

speed = 1
k = 0

while (robot.step(timestep) != -1):
 
    # Left Leg 1
    #ll1m.setVelocity(speed)
    #ll1=ll1ps.getValue()
    #ll1_deg=180/3.14*ll1
    #print(ll1_deg)
    
    # Left Leg 2
    #ll2m.setVelocity(speed)
    #ll2=ll2ps.getValue()
    #ll2_deg=180/3.14*ll2
    #print(ll2_deg)
    
    # Left Leg 3
    #ll3m.setVelocity(speed)
    #ll3=ll3ps.getValue()
    #ll3_deg=180/3.14*ll3
    #print(ll3_deg)
    
    # Left Leg 4
    #ll4m.setVelocity(speed)
    #ll4=ll4ps.getValue()
    #ll4_deg=180/3.14*ll4
    #print(ll4_deg)

    # Left Leg 5
    #ll5m.setVelocity(speed)
    #ll5=ll6ps.getValue()
    #ll5_deg=180/3.14*ll5
    #print(ll5_deg)
    
    # Left Leg 6
    #ll6m.setVelocity(speed)
    #ll6=ll6ps.getValue()
    #ll6_deg=180/3.14*ll6
    #print(ll6_deg)
    
    # Right Leg 1
    #rl1m.setVelocity(speed)
    #rl1=rl1ps.getValue()
    #rl1_deg=180/3.14*rl1
    #print(rl1_deg)
    
    # Right Leg 2
    #rl2m.setVelocity(speed)
    #rl2=rl2ps.getValue()
    #rl2_deg=180/3.14*rl2
    #print(rl2_deg)
    
    # Right Leg 3
    #rl3m.setPosition(90.0)
    rl3m.setVelocity(-speed)
    rl3=rl3ps.getValue()
    rl3_deg=180/3.14*rl3
    print(rl3_deg)
    
    # Right Leg 4
    #rl4m.setVelocity(speed)
    #rl4=rl4ps.getValue()
    #rl4_deg=180/3.14*rl4
    #print(rl4_deg)

    # Right Leg 5
    #rl5m.setPosition(90.0)
    #rl5m.setVelocity(speed)
    #rl5=rl6ps.getValue()
    #rl5_deg=180/3.14*rl5
    #print(rl5_deg)
    
    # Right Leg 6
    #rl6m.setVelocity(speed)
    #rl6=rl6ps.getValue()
    #rl6_deg=180/3.14*rl6
    #print(rl6_deg)
