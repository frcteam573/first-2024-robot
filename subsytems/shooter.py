import math

import commands2
import wpilib
import wpilib.drive
import rev

from config import shooter_threshold

def remap(value: float, threshold: float) -> float:
    if abs(value) > threshold:
        value = value / abs(value) * threshold
    return value

def deadband(value: float, threshold: float) -> float:
    if abs(value) < threshold:
        value = 0
    return value

class Shooter(commands2.SubsystemBase):

    def __init__(self) -> None:
        super().__init__()
        
        self.m_shooter1 = rev.CANSparkMax(43, rev.CANSparkMax.MotorType.kBrushless)
        self.m_shooter2 = rev.CANSparkMax(40, rev.CANSparkMax.MotorType.kBrushless)
        self.m_shooter2.follow(self.m_shooter1)
        self.shooterPID1 = self.m_shooter1.getPIDController()
        self.shooterPID1.setP(0.025) # find these values when built
        self.shooterPID1.setI(0.000000000001) # find these values when built
        self.shooterPID1.setIZone(0)
        self.shooterPID1.setD(0.01) # find these values when built
        self.shooterPID1.setFF(0)
        
        # self.shooterPID2 = self.m_shooter2.getPIDController()
        # self.shooterPID2.setP(0.0007) # find these values when built
        # self.shooterPID2.setI(0.00001) # find these values when built
        # self.shooterPID2.setD(0.0) # find these values when built
        self.s_shooterEncoder1 = self.m_shooter1.getEncoder()
        self.s_shooterEncoder2 = self.m_shooter2.getEncoder()
                
    def setShooterRPM(self, speed: float) -> bool:
        '''Sets the RPM of the shooter motors.
        
        Args:
            speed: The RPM to set the motors to, -5000 to 5000.
        '''
        speed = -speed
        self.at_speed = False
        #print("target:", speed, "actual:", self.s_shooterEncoder1.getVelocity(), self.s_shooterEncoder2.getVelocity())
        
        if speed == 0:
            self.m_shooter1.set(0)
            wpilib.SmartDashboard.putBoolean("Shooter at speed", True)
        else:
            self.shooterPID1.setReference(speed, rev.CANSparkMax.ControlType.kVelocity)
            # self.m_shooter1.set(-1)

            wpilib.SmartDashboard.putString("Shooter 1 RPM", str(self.s_shooterEncoder1.getVelocity()))
            wpilib.SmartDashboard.putString("Shooter 2 RPM", str(self.s_shooterEncoder2.getVelocity()))

            ratio_1 = abs(self.s_shooterEncoder1.getVelocity() / speed)
            ratio_2 = abs(self.s_shooterEncoder2.getVelocity() / speed)
            min = 1 - shooter_threshold
            max = 1 + shooter_threshold
            if min < ratio_1 < max and min < ratio_2 < max and speed != 0:
                wpilib.SmartDashboard.putBoolean("Shooter at speed", True)
                self.at_speed = True
            else:
                wpilib.SmartDashboard.putBoolean("Shooter at speed", False)
        return self.at_speed
    
