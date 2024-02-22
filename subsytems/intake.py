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

class Intake(commands2.SubsystemBase):

    def __init__(self) -> None:
        super().__init__()
                
        self.s_claw_lightgate = wpilib.DigitalInput(0)
        
        self.m_intake1 = rev.CANSparkMax(41, rev.CANSparkMax.MotorType.kBrushless)
        
        self.m_transfer = rev.CANSparkMax(44, rev.CANSparkMax.MotorType.kBrushless)        
        
    def setIntakeSpeed(self, speed: float) -> None:
        '''Sets the speed of the intake motors.
        
        Args:
            speed: The speed to set the motors to, -1 to 1.
            
        '''
        self.m_intake1.set(speed)
        self.m_transfer.set(-.25 * speed)
        #print("HHHHHHHH")
        
    def setTransferSpeed(self, speed: float) -> None:
        '''Sets the speed of the transfer motor.
        
        Args:
            speed: The speed to set the motor to, -1 to 1.
        '''
        # if wpilib.SmartDashboard.getBoolean("Ready to shoot", False):
        self.m_transfer.set(speed)
        self.m_intake1.set(-speed)
        print("TRANSFERRRR")
        # else:
        #     self.m_transfer.set(0)
        #     self.m_intake1.set(0)