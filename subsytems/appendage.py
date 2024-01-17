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
        
        self.wristMin = 0
        self.wristMax = 7.5

        self.m_roller1 = rev.CANSparkMax(14, rev.CANSparkMax.MotorType.kBrushless)
        self.m_roller2 = rev.CANSparkMax(15, rev.CANSparkMax.MotorType.kBrushless)
        
        self.m_wrist = rev.CANSparkMax(18, rev.CANSparkMax.MotorType.kBrushless)
        
        self.wristEncoder = self.m_wrist.getEncoder()
        
        self.p_rollerCylinder = wpilib.DoubleSolenoid(19, wpilib.PneumaticsModuleType.CTREPCM, 1, 0)
        
        
    def setIntake(self, speed: float) -> None:
        self.m_roller1.set(speed)
        self.m_roller2.set(-1*speed)
        
    def setWrist(self, speed: float) -> None:
        out = remap(speed, .85)
        print1=out
        out = deadband(out, 0.05)
        print2=out
        cur = self.wristEncoder.getPosition()
        print4 = "cur: " + str(cur)
        
        print3=""
        if ((cur < self.wristMin and out < 0) or (cur > self.wristMax and out > 0)):
            out = 0
            print3 = "stopped"

        
        
        self.m_wrist.set(out)
        
        print(print1, print2, print3, print4)

    def pneumaticsIn(self) -> None:
        self.p_rollerCylinder.set(wpilib.DoubleSolenoid.Value.kForward)
        
    def pneumaticsOut(self) -> None:
        self.p_rollerCylinder.set(wpilib.DoubleSolenoid.Value.kReverse)