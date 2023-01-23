import numpy as np
from RobotArm import RobotArm

Robot = RobotArm()

Robot.goTo(300, 0, 300)
Robot.goHome()
Robot.goLinearlyTo(400, 0, 200)
