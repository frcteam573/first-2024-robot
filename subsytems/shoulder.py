import math

import commands2
import wpilib
from wpilib.shuffleboard import Shuffleboard, BuiltInWidgets
import wpilib.drive
import rev
#from phoenix6.hardware.cancoder import CANcoder as CANCoder
from config import shoulder_threshold
from units.SI import meters_to_inches
from wpimath.controller import PIDController

def remap(value: float, threshold: float) -> float:
    if abs(value) > threshold:
        value = value / abs(value) * threshold
    return value

def deadband(value: float, threshold: float) -> float:
    if abs(value) < threshold:
        value = 0
    return value

class Shoulder(commands2.SubsystemBase):

    def __init__(self) -> None:
        super().__init__()
        
        #double solenoid, pcm (pnematic control module)
        self.p_shoulderlock = wpilib.DoubleSolenoid(19, wpilib.PneumaticsModuleType.CTREPCM, 4, 5)
        self.p_shoulderlock.set(wpilib.DoubleSolenoid.Value.kReverse)
        
        self.m_shoulder1 = rev.CANSparkMax(47, rev.CANSparkMax.MotorType.kBrushless)
        self.m_shoulder2 = rev.CANSparkMax(48, rev.CANSparkMax.MotorType.kBrushless)
        self.m_shoulder2.follow(self.m_shoulder1, invert=True)

        # self.PID_tab = Shuffleboard.getTab("PID")
        self.shoulderPID_kP = 1.0 # find these values when built
        self.shoulderPID_kI = 0.0 # find these values when built
        self.shoulderPID_kD = 0.06 # find these values when built
        
        self.shoulderPID = PIDController(self.shoulderPID_kP,self.shoulderPID_kI,self.shoulderPID_kD)
        # self.PID_config = self.PID_tab.add("Shoulder PID", self.shoulderPID).withWidget(BuiltInWidgets.kPIDController).getEntry()
        self.shoulderPID.setTolerance(shoulder_threshold)
        
        self.minShoulderAngle = 0 # find these values when built
        self.maxShoulderAngle = 100 # find these values when built
        self.s_shoulderAlternateEncoder = self.m_shoulder1.getAlternateEncoder(8192)
        
                
    def setShoulderSpeed(self, speed: float):
        '''Sets the speed of the shoulder motors.
        
        Args:
            speed: The speed to set the motors to, -1 to 1.
        '''
        wpilib.SmartDashboard.putString("S_Shoulder Angle", str(self.s_shoulderAlternateEncoder.getPosition()))
        if abs(speed) > 0.95:
            speed = 0.95* speed/abs(speed)
        
        self.m_shoulder1.set(speed)
        
        # print("Shoulder Speed: "+ str(speed))

    def setShoulderLocks(self, lock: bool):
        if lock:
            self.p_shoulderlock.set(wpilib.DoubleSolenoid.Value.kForward)
        else:
            self.p_shoulderlock.set(wpilib.DoubleSolenoid.Value.kReverse)
    
    
    def setShoulderAngle(self, angle: float) -> None:
        '''Sets the angle of the shoulder motors.
        
        Args:
            angle: The angle to set the motors to in degrees.
        '''
        angle += wpilib.SmartDashboard.getNumber("Shoulder Trim", 0) / 180 * math.pi
        
        at_pos = False
        if angle < self.minShoulderAngle:
            angle = self.minShoulderAngle
        elif angle > self.maxShoulderAngle:
            angle = self.maxShoulderAngle
        
        #rotations = angle / 360
        speed = -self.shoulderPID.calculate(self.s_shoulderAlternateEncoder.getPosition(), angle)
        self.setShoulderSpeed(speed * (2 if speed > .1 else 1))

        if self.shoulderPID.atSetpoint():
            at_pos = True
            #self.p_shoulderlock.set(wpilib.DoubleSolenoid.Value.kForward)
            wpilib.SmartDashboard.putBoolean("Shoulder at angle", True)
        else:
            wpilib.SmartDashboard.putBoolean("Shoulder at angle", False)
            #self.p_shoulderlock.set(wpilib.DoubleSolenoid.Value.kReverse)
            
        return at_pos
            
            
    def calculateShoulderAngle(self, distance_to_speaker: float) -> float:
        '''Calculates the angle of the shoulder motors.
        
        Args:
            distance_to_speaker: The distance to the speaker in meters.
            blue_team: Whether the robot is on the blue team.
            
        Returns:
            radians
        '''
        # improve this
        distance_to_speaker *= meters_to_inches
        return 1.41 + -9.67E-03 * distance_to_speaker + 2.7E-05 * distance_to_speaker**2
    
    def changeShoulderTrim(self, value: float) -> None:
        '''Changes the trim of the shoulder.
        
        Args:
            value: The value to change the trim by.
        '''
        trim = wpilib.SmartDashboard.getNumber("Shoulder Trim", 0)
        wpilib.SmartDashboard.putNumber("Shoulder Trim", trim + value)