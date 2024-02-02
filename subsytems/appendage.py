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

        self.m_intake1 = rev.CANSparkMax(41, rev.CANSparkMax.MotorType.kBrushless)
        self.m_intake2 = rev.CANSparkMax(42, rev.CANSparkMax.MotorType.kBrushless)
        self.m_intake2.follow(self.m_intake1, invert=True)
        
        self.m_transfer = rev.CANSparkMax(44, rev.CANSparkMax.MotorType.kBrushless)
        
        self.m_shooter1 = rev.CANSparkMax(43, rev.CANSparkMax.MotorType.kBrushless)
        self.m_shooter2 = rev.CANSparkMax(40, rev.CANSparkMax.MotorType.kBrushless)
        self.m_shooter2.follow(self.m_shooter1, invert=True)
        self.shooterPID = self.m_shooter1.getPIDController()
        self.shooterPID.setP(0.00005) # find these values when built
        self.shooterPID.setI(0.0000005) # find these values when built
        self.shooterPID.setD(0.0) # find these values when built
        
        # self.m_climber1 = rev.CANSparkMax(45, rev.CANSparkMax.MotorType.kBrushless)
        # self.m_climber2 = rev.CANSparkMax(46, rev.CANSparkMax.MotorType.kBrushless)
        # self.m_climber2.follow(self.m_climber1, invert=True)
        # self.s_climberEncoder = self.m_climber1.getEncoder()
        # self.climbermin = 0 # find these values when built
        # self.climbermax = 100 # find these values when built
        
        # self.m_shoulder1 = rev.CANSparkMax(47, rev.CANSparkMax.MotorType.kBrushless)
        # self.m_shoulder2 = rev.CANSparkMax(48, rev.CANSparkMax.MotorType.kBrushless)
        # self.m_shoulder2.follow(self.m_shoulder1, invert=True)
        # self.shoulderPID = self.m_shoulder1.getPIDController()
        # self.shoulderPID.setP(0.00005) # find these values when built
        # self.shoulderPID.setI(0.0000005) # find these values when built
        # self.shoulderPID.setD(0.0) # find these values when built
        # self.minShoulderAngle = 0 # find these values when built
        # self.maxShoulderAngle = 100 # find these values when built
        
        
    def setIntakeSpeed(self, speed: float) -> None:
        '''Sets the speed of the intake motors.
        
        Args:
            speed: The speed to set the motors to, -1 to 1.
            
        '''
        self.m_intake1.set(speed)
        
    def setTransferSpeed(self, speed: float) -> None:
        '''Sets the speed of the transfer motor.
        
        Args:
            speed: The speed to set the motor to, -1 to 1.
        '''
        self.m_transfer.set(speed)
        self.m_intake1.set(-speed)
        
    def setShooterRPM(self, speed: float) -> None:
        '''Sets the RPM of the shooter motors.
        
        Args:
            speed: The RPM to set the motors to, -11000 to 11000.
        '''
        if speed == 0:
            self.m_shooter1.set(0)
        else:
            self.shooterPID.setReference(speed, rev.CANSparkMax.ControlType.kVelocity)
        
    def setClimberSpeed(self, speed: float) -> None:
        '''Sets the speed of the climber motors.
        
        Args:
            speed: The speed to set the motors to, -1 to 1.
        '''
        if self.s_climberEncoder.getPosition() < self.climbermin and speed < 0:
            self.m_climber1.set(0)
        elif self.s_climberEncoder.getPosition() > self.climbermax and speed > 0:
            self.m_climber1.set(0)
        else:
            self.m_climber1.set(speed)
    
    def setShoulderAngle(self, angle: float) -> None:
        '''Sets the angle of the shoulder motors.
        
        Args:
            angle: The angle to set the motors to in degrees.
        '''
        
        if angle < self.minShoulderAngle:
            angle = self.minShoulderAngle
        elif angle > self.maxShoulderAngle:
            angle = self.maxShoulderAngle
        
        rotations = angle / 360
        self.shoulderPID.setReference(rotations, rev.CANSparkMax.ControlType.kPosition)
        
    def calculateShoulderAngle(self, distance_to_speaker: float) -> float:
        '''Calculates the angle of the shoulder motors.
        
        Args:
            distance_to_speaker: The distance to the speaker in meters.
            blue_team: Whether the robot is on the blue team.
        '''
        ...
        # implement this