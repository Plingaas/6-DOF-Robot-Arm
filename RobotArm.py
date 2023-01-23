import IK
import numpy as np

class RobotArm():

    def __init__(self):
        self.pos = [0, 0, 0]
        self.home = [591.829999, 0, 169.77]
        self.angles = [0, 0, 0]

    def printInfo(self):
        print("========================= NEW POSITION =========================")
        print(f"x: {self.pos[0]}        y: {self.pos[1]}        z: {self.pos[2]}")
        print(f"θ1: {self.angles[0]}    θ2: {self.angles[1]}    θ3: {self.angles[2]}")
        print("================================================================")
        print()

    def isWithinWorkspace(self, x, y, z):
        try:
            IK.IK(x, y, z)
        except:
            print(f"Unable to reach position {[x, y, z]}.")
            return False
        return True

    def goTo(self, x, y, z, out = True):

        if not self.isWithinWorkspace(x, y, z):
            return
        
        a1, a2, a3 = IK.IK(x, y, z)

        self.angles = [a1, a2, a3]
        self.pos = [x, y, z]

        if out:
            self.printInfo()

    def goHome(self):
        self.goTo(self.home[0], self.home[1], self.home[2])
    
    def goLinearlyTo(self, x, y, z):

        if not self.isWithinWorkspace(x, y, z):
            return

        # resolution variable (points/mm)
        ppmm = 10

        dx = x - self.pos[0]
        dy = y - self.pos[1]
        dz = z - self.pos[2]

        dist = np.sqrt(dx**2 + dy**2 + dz**2)
        points = int(dist*ppmm)

        dx /= points
        dy /= points
        dz /= points

        counter = 0
        while counter < points:
            _x = self.pos[0] + dx
            _y = self.pos[1] + dy
            _z = self.pos[2] + dz
            self.goTo(_x, _y, _z, False)
            counter += 1
        self.goTo(x, y, z)