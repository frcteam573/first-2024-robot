import math

import commands2
import wpilib
from wpilib.shuffleboard import Shuffleboard, BuiltInWidgets
import wpilib.drive
import rev
#from phoenix6.hardware.cancoder import CANcoder as CANCoder
from config import shoulder_threshold_lowest, shoulder_threshold_highest, shoulder_threshold_lowest_distance, shoulder_threshold_highest_distance
from units.SI import meters_to_inches, inches_to_meters
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
        self.p_shoulderlock.set(wpilib.DoubleSolenoid.Value.kForward)
        
        self.m_shoulder1 = rev.CANSparkMax(47, rev.CANSparkMax.MotorType.kBrushless)
        self.m_shoulder2 = rev.CANSparkMax(48, rev.CANSparkMax.MotorType.kBrushless)
        self.m_shoulder2.follow(self.m_shoulder1, invert=True)

        # self.PID_tab = Shuffleboard.getTab("PID")
        self.shoulderPID_kP = 1.0 # find these values when built
        self.shoulderPID_kI = 0.0001 # find these values when built
        self.shoulderPID_kD = 0.06 # find these values when built
       
        
        self.shoulderPID = PIDController(self.shoulderPID_kP,self.shoulderPID_kI,self.shoulderPID_kD)
        # self.PID_config = self.PID_tab.add("Shoulder PID", self.shoulderPID).withWidget(BuiltInWidgets.kPIDController).getEntry()
        #self.shoulderPID.setTolerance(shoulder_threshold)
        self.shoulderPID.setIZone(0.1)
        
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
    
    
    def setShoulderAngle(self, angle: float, distance: float = shoulder_threshold_lowest_distance) -> bool:
        '''Sets the angle of the shoulder motors.
        
        Args:
            angle: The angle to set the motors to in degrees.
        '''
        #angle += wpilib.SmartDashboard.getNumber("Shoulder Trim", 0) / 180 * math.pi
        self.at_pos = False
        if angle < self.minShoulderAngle:
            angle = self.minShoulderAngle
        elif angle > self.maxShoulderAngle:
            angle = self.maxShoulderAngle
        
        #rotations = angle / 360
        speed = -self.shoulderPID.calculate(self.s_shoulderAlternateEncoder.getPosition(), angle)
        self.setShoulderSpeed(speed * (2 if speed > .1 else 1))
        self.shoulder_threshold = shoulder_threshold_lowest
        if distance < shoulder_threshold_lowest_distance:
            if distance < shoulder_threshold_highest_distance:
                self.shoulder_threshold = shoulder_threshold_highest
            else:
                slope = (shoulder_threshold_highest-shoulder_threshold_lowest)/(shoulder_threshold_highest_distance-shoulder_threshold_lowest_distance)
                b = shoulder_threshold_lowest- slope*shoulder_threshold_lowest_distance
                self.shoulder_threshold = slope*distance + b

        if abs(self.s_shoulderAlternateEncoder.getPosition() - angle) < self.shoulder_threshold:
            self.at_pos = True
            #self.p_shoulderlock.set(wpilib.DoubleSolenoid.Value.kForward)
            wpilib.SmartDashboard.putBoolean("Shoulder at angle", True)
        else:
            wpilib.SmartDashboard.putBoolean("Shoulder at angle", False)
            #self.p_shoulderlock.set(wpilib.DoubleSolenoid.Value.kReverse)
        #print(str(self.at_pos))
        return self.at_pos
            
            
    def calculateShoulderAngle(self, distance_to_speaker: float) -> float:
        '''Calculates the angle of the shoulder motors.
        
        Args:
            distance_to_speaker: The distance to the speaker in meters.
            blue_team: Whether the robot is on the blue team.
            
        Returns:
            radians
        '''
        # improve this
        return 1.22 + -0.3 * distance_to_speaker + 0.0347 * distance_to_speaker**2 + wpilib.SmartDashboard.getNumber("Shoulder Trim", 0)
    
    def changeShoulderTrim(self, value: float) -> None:
        '''Changes the trim of the shoulder.
        
        Args:
            value: The value to change the trim by.
        '''
        trim = wpilib.SmartDashboard.getNumber("Shoulder Trim", 0)
        #print("TRIM" + str(trim))
        wpilib.SmartDashboard.putNumber("Shoulder Trim", trim + value)

    def getShoulderPos(self) -> float:

        return self.s_shoulderAlternateEncoder.getPosition()