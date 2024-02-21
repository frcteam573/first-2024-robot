import math

import commands2
import wpilib
import wpilib.drive
import rev
#from phoenix6.hardware.cancoder import CANcoder as CANCoder
from config import shooter_threshold, shoulder_threshold, shoulder_min, shoulder_max

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
        
        #double solenoid, pcm (pnematic control module)
        self.p_shoulderlock = wpilib.DoubleSolenoid(19, wpilib.PneumaticsModuleType.CTREPCM, 4, 5)
        self.p_climberlock = wpilib.DoubleSolenoid(19, wpilib.PneumaticsModuleType.CTREPCM, 0, 1)
        self.p_climberlock.set(wpilib.DoubleSolenoid.Value.kForward)
        self.p_shoulderlock.set(wpilib.DoubleSolenoid.Value.kForward)
        
        self.s_claw_lightgate = wpilib.DigitalInput(0)
        
        self.m_intake1 = rev.CANSparkMax(41, rev.CANSparkMax.MotorType.kBrushless)
        
        self.m_transfer = rev.CANSparkMax(44, rev.CANSparkMax.MotorType.kBrushless)
        
        self.m_shooter1 = rev.CANSparkMax(43, rev.CANSparkMax.MotorType.kBrushless)
        self.m_shooter2 = rev.CANSparkMax(40, rev.CANSparkMax.MotorType.kBrushless)
        self.m_shooter2.follow(self.m_shooter1)
        self.shooterPID = self.m_shooter1.getPIDController()
        self.shooterPID.setP(0.00005) # find these values when built
        self.shooterPID.setI(0.0000005) # find these values when built
        self.shooterPID.setD(0.0) # find these values when built
        self.s_shooterEncoder1 = self.m_shooter1.getEncoder()
        self.s_shooterEncoder2 = self.m_shooter2.getEncoder()
        
        self.m_climber1 = rev.CANSparkMax(45, rev.CANSparkMax.MotorType.kBrushless)
        self.m_climber2 = rev.CANSparkMax(46, rev.CANSparkMax.MotorType.kBrushless)
        self.m_climber2.follow(self.m_climber1, invert= True)
        self.s_climber1Encoder = self.m_climber1.getEncoder()
        self.s_climberEncoderAlt = self.m_climber1.getAlternateEncoder(8192)
        self.climbermin = -100000 # find these values when built
        self.climbermax = 1000000 # find these values when built
        
        self.m_shoulder1 = rev.CANSparkMax(47, rev.CANSparkMax.MotorType.kBrushless)
        self.m_shoulder2 = rev.CANSparkMax(48, rev.CANSparkMax.MotorType.kBrushless)
        self.m_shoulder2.follow(self.m_shoulder1, invert=True)
        self.shoulderPID = self.m_shoulder1.getPIDController()
        self.shoulderPID.setP(0.00005) # find these values when built
        self.shoulderPID.setI(0.0000005) # find these values when built
        self.shoulderPID.setD(0.0) # find these values when built
        self.minShoulderAngle = 0 # find these values when built
        self.maxShoulderAngle = 100 # find these values when built
        self.s_shoulderAlternateEncoder = self.m_shoulder1.getAlternateEncoder(8192)
        
        
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
        # else:
        #     self.m_transfer.set(0)
        #     self.m_intake1.set(0)
        
    def setShooterRPM(self, speed: float) -> None:
        '''Sets the RPM of the shooter motors.
        
        Args:
            speed: The RPM to set the motors to, -11000 to 11000.
        '''
        speed = -speed
        
        #print("target:", speed, "actual:", self.s_shooterEncoder1.getVelocity(), self.s_shooterEncoder2.getVelocity())
        
        if speed == 0:
            self.m_shooter1.set(0)
            wpilib.SmartDashboard.putBoolean("Shooter at speed", True)
        else:
            self.shooterPID.setReference(speed, rev.CANSparkMax.ControlType.kVelocity)
            #self.m_shooter1.set(-1)

            wpilib.SmartDashboard.putString("Shooter 1 RPM", str(self.s_shooterEncoder1.getVelocity()))
            wpilib.SmartDashboard.putString("Shooter 2 RPM", str(self.s_shooterEncoder2.getVelocity()))

            ratio_1 = self.s_shooterEncoder1.getVelocity() / speed
            ratio_2 = self.s_shooterEncoder2.getVelocity() / speed
            min = 1 - shooter_threshold
            max = 1 + shooter_threshold
            if min < ratio_1 < max and min < ratio_2 < max and speed != 0:
                wpilib.SmartDashboard.putBoolean("Shooter at speed", True)
            else:
                wpilib.SmartDashboard.putBoolean("Shooter at speed", False)
        
    def setClimberSpeed(self, speed: float) -> None:
        '''Sets the speed of the climber motors.
        
        Args:
            speed: The speed to set the motors to, -1 to 1.
        '''
        wpilib.SmartDashboard.putString("S_Climber Pos Alt", str(self.s_climberEncoderAlt.getPosition()))
        wpilib.SmartDashboard.putString("S_Climber Pos Motor", str(self.s_climber1Encoder.getPosition()))
        if self.s_climberEncoder.getPosition() < self.climbermin and speed < 0:
            self.m_climber1.set(0)
            self.p_climberlock.set(wpilib.DoubleSolenoid.Value.kForward)
        elif self.s_climberEncoder.getPosition() > self.climbermax and speed > 0:
            self.m_climber1.set(0)
            self.p_climberlock.set(wpilib.DoubleSolenoid.Value.kForward)
        else:
            self.m_climber1.set(speed)
            if speed > 0:
                self.p_climberlock.set(wpilib.DoubleSolenoid.Value.kReverse)
            else:
                self.p_climberlock.set(wpilib.DoubleSolenoid.Value.kForward)
                
    def setShoulderSpeed(self, speed: float):
        '''Sets the speed of the shoulder motors.
        
        Args:
            speed: The speed to set the motors to, -1 to 1.
        '''

        wpilib.SmartDashboard.putString("S_Shoulder Angle", str(self.s_shoulderAlternateEncoder.getPosition()))
        if abs(speed) > 0.7:
            speed = 0.7* speed/abs(speed)
        
        self.m_shoulder1.set(speed)

        if abs(speed) < 0.1:
            self.p_shoulderlock.set (wpilib.DoubleSolenoid.Value.kForward)
        else:
            self.p_shoulderlock.set (wpilib.DoubleSolenoid.Value.kReverse)
    
    
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
        if abs(self.s_shoulderAlternateEncoder.getPosition() - angle) < shoulder_threshold:
            wpilib.SmartDashboard.putBoolean("Shoulder at angle", True)
        else:
            wpilib.SmartDashboard.putBoolean("Shoulder at angle", False)
            
        if self.m_shoulder1.get() == 0:
            self.p_shoulderlock.set (wpilib.DoubleSolenoid.Value.kForward)  
        else:
            self.p_shoulderlock.set (wpilib.DoubleSolenoid.Value.kReverse)
            
    def calculateShoulderAngle(self, distance_to_speaker: float) -> float:
        '''Calculates the angle of the shoulder motors.
        
        Args:
            distance_to_speaker: The distance to the speaker in meters.
            blue_team: Whether the robot is on the blue team.
            
        Returns:
            radians
        '''
        # implement this
        return 45