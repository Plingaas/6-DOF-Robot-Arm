import numpy as np

# JOINT ANGLES
a1 = 169.77 #
a2 = 64.2
a3 = 0
a4 = 305 # Joint 2 arm 305mm
a5 = 0
a6 = 222.63 # Joint 3 arm 222.63mm

J1_LOWER_LIMIT = -170
J1_UPPER_LIMIT = 170

J2_LOWER_LIMIT = 0
J2_UPPER_LIMIT = 132

J3_LOWER_LIMIT = -140
J3_UPPER_LIMIT = 1

TO_DEGREES = 180/np.pi

def IK(x, y, z):
    phi0 = 90 - np.arctan2(y, x) # eq 1

    theta1 = np.arctan2( (y - (a3-a5)*np.sin(phi0)), (x - (a3-a5)*np.cos(phi0)) ) # eq 2

    z1_3 = z - a1 # eq 3

    x0_1 = a2*np.cos(theta1) - a3*np.sin(theta1) # eq 4

    x1_3 = x - x0_1 # eq 5

    phi2 = np.arctan2(z1_3, x1_3) # eq6
    r1 = np.sqrt( x1_3**2 + z1_3**2) # eq 7


    num = (a6**2 - r1**2 - a4**2)/(-2*r1*a4)
    if not (-1 <= num <= 1):
        raise ValueError
        
    phi1 = np.arccos( num ) # eq 8
    
    
    inverse = False
    
    # Not sure if this is needed, but it checks both solutions
    theta2 = phi2 - phi1 # eq 9
    if theta2*TO_DEGREES < J2_LOWER_LIMIT or theta2*TO_DEGREES > J2_UPPER_LIMIT:
        inverse = True
        theta2 = phi2 + phi1

    num = (r1**2-a4**2-a6**2)/(-2*a4*a6)
    phi3 = np.arccos( num ) # eq 10
    if not (-1 <= num <= 1):
        raise ValueError

    if inverse:
        theta3 = -np.pi + phi3 
    else:
        theta3 = np.pi - phi3 # eq 11

    
    theta1 *= TO_DEGREES
    theta2 *= TO_DEGREES
    theta3 *= TO_DEGREES

    if not (J1_LOWER_LIMIT <= theta1 <= J1_UPPER_LIMIT):
        print("Outside workspace")
        raise ValueError
    if not (J2_LOWER_LIMIT <= theta2 <= J2_UPPER_LIMIT):
        print("Outside workspace")
        raise ValueError
    if not (J3_LOWER_LIMIT <= theta3 <= J3_UPPER_LIMIT):
        print("Outside workspace")
        raise ValueError

    return theta1, theta2, theta3