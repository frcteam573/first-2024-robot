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

class Appendage(commands2.SubsystemBase):

    def __init__(self) -> None:
        super().__init__()

        self.m_intake1 = rev.CANSparkMax(14, rev.CANSparkMax.MotorType.kBrushless)
        self.m_intake2 = rev.CANSparkMax(15, rev.CANSparkMax.MotorType.kBrushless)
        self.m_transfer = rev.CANSparkMax(16, rev.CANSparkMax.MotorType.kBrushless)
        self.m_shooter1 = rev.CANSparkMax(17, rev.CANSparkMax.MotorType.kBrushless)
        self.m_shooter2 = rev.CANSparkMax(18, rev.CANSparkMax.MotorType.kBrushless)
        self.m_shooter2.follow(self.m_shooter1)
        self.s_shooterEncoder1 = self.m_shooter1.getEncoder()
        self.shooterPID = self.m_shooter1.getPIDController()
        self.shooterPID.setP(0.00005)
        self.shooterPID.setI(0.0000005)
        self.shooterPID.setD(0.0)
        
    def setIntake(self, speed: float) -> None:
        self.m_intake1.set(speed)
        self.m_intake2.set(speed)
        
    def setTransfer(self, speed: float) -> None:
        self.m_transfer.set(speed)
        
    def setShooter(self, speed: float) -> None:
        if speed == 0:
            self.m_shooter1.set(0)
        else:
            self.shooterPID.setReference(speed, rev.CANSparkMax.ControlType.kVelocity)
        print("setting shooter speed to", self.RPM)
        
    