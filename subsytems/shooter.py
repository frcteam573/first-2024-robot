import math

import commands2
import wpilib
from wpilib.shuffleboard import Shuffleboard, BuiltInWidgets
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
        
        self.kp = 0.015
        self.ki = 0.000000000001
        self.kd = 0.01
        self.izone = 100
        self.ff = 0
        self.m_shooter1 = rev.CANSparkMax(43, rev.CANSparkMax.MotorType.kBrushless)
        self.m_shooter2 = rev.CANSparkMax(40, rev.CANSparkMax.MotorType.kBrushless)
        # self.m_shooter2.follow(self.m_shooter1)
        self.shooterPID1 = self.m_shooter1.getPIDController()
        self.shooterPID1.setP(self.kp) # find these values when built
        self.shooterPID1.setI(self.ki) # find these values when built
        self.shooterPID1.setIZone(self.izone)
        self.shooterPID1.setD(self.kd) # find these values when built
        self.shooterPID1.setFF(self.ff)
        self.shooterPID2 = self.m_shooter2.getPIDController()
        self.shooterPID2.setP(self.kp) # find these values when built
        self.shooterPID2.setI(self.ki) # find these values when built
        self.shooterPID2.setIZone(self.izone)
        self.shooterPID2.setD(self.kd) # find these values when built
        self.shooterPID2.setFF(self.ff)
        self.s_shooterEncoder1 = self.m_shooter1.getEncoder()
        self.s_shooterEncoder2 = self.m_shooter2.getEncoder()
        
        self.pid_graphs = Shuffleboard.getTab("Shooter PID")
        self.graph1 = self.pid_graphs.add("Shooter 1", 0).withWidget(BuiltInWidgets.kGraph).getEntry()
        self.graph2 = self.pid_graphs.add("Shooter 2", 0).withWidget(BuiltInWidgets.kGraph).getEntry()
        self.pid_settings_kp = self.pid_graphs.add("kp", self.kp).getEntry()
        self.pid_settings_ki = self.pid_graphs.add("ki", self.ki).getEntry()
        self.pid_settings_kd = self.pid_graphs.add("kd", self.kd).getEntry()
        
    def setShooterRPM(self, speed: float) -> bool:
        '''Sets the RPM of the shooter motors.
        
        Args:
            speed: The RPM to set the motors to, -5000 to 5000.
        '''
        kp = self.pid_settings_kp.getDouble(self.kp)
        ki = self.pid_settings_ki.getDouble(self.ki)
        kd = self.pid_settings_kd.getDouble(self.kd)
        
        self.shooterPID1.setP(kp)
        self.shooterPID1.setI(ki)
        self.shooterPID1.setD(kd)
        self.shooterPID2.setP(kp)
        self.shooterPID2.setI(ki)
        self.shooterPID2.setD(kd)
        
        self.graph1.setDouble(-self.s_shooterEncoder1.getVelocity())
        self.graph2.setDouble(-self.s_shooterEncoder2.getVelocity())
        
        self.at_speed = False
        #print("target:", speed, "actual:", self.s_shooterEncoder1.getVelocity(), self.s_shooterEncoder2.getVelocity())
        
        if speed == 0:
            self.m_shooter1.set(0)
            self.m_shooter2.set(0)
            wpilib.SmartDashboard.putBoolean("Shooter at speed", True)
        else:
            self.m_shooter1.set(1)
            self.m_shooter2.set(1)
            # self.shooterPID1.setReference(speed, rev.CANSparkMax.ControlType.kVelocity)
            # self.shooterPID2.setReference(speed, rev.CANSparkMax.ControlType.kVelocity)

            wpilib.SmartDashboard.putNumber("Shooter 1 RPM", self.s_shooterEncoder1.getVelocity())
            wpilib.SmartDashboard.putNumber("Shooter 2 RPM", self.s_shooterEncoder2.getVelocity())

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
    
