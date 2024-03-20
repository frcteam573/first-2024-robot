import math

import commands2
import wpilib
import wpilib.drive
import rev

def remap(value: float, threshold: float) -> float:
    if abs(value) > threshold:
        value = value / abs(value) * threshold
    return value

def deadband(value: float, threshold: float) -> float:
    if abs(value) < threshold:
        value = 0
    return value

class Trap(commands2.SubsystemBase):

    def __init__(self) -> None:
        super().__init__()
        
        #double solenoid, pcm (pnematic control module)

        self.servo = wpilib.Servo(1)

    def StopTrap(self) -> None:

        self.servo.setAngle(90) #Set Trap Hood to off.
        #print("Stop Hood") 

        
    def ExtendTrap(self) -> None:
        '''Sets the speed of the climber motors.
        
        Args:
            speed: The speed to set the motors to, -1 to 1.
        '''
        #print("Extend Hood") 
        self.servo.setAngle(1)

    def RetractTrap(self) -> None:
        '''Sets the speed of the climber motors.
        
        Args:
            speed: The speed to set the motors to, -1 to 1.
        '''
                  
        self.servo.setAngle(179)



