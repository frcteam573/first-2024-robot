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

class Climber(commands2.SubsystemBase):

    def __init__(self) -> None:
        super().__init__()
        
        #double solenoid, pcm (pnematic control module)

        self.p_climberlock = wpilib.DoubleSolenoid(19, wpilib.PneumaticsModuleType.CTREPCM, 1, 0)
        self.p_climberlock.set(wpilib.DoubleSolenoid.Value.kReverse)

        self.m_climber1 = rev.CANSparkMax(45, rev.CANSparkMax.MotorType.kBrushless)
        self.m_climber2 = rev.CANSparkMax(46, rev.CANSparkMax.MotorType.kBrushless)
        self.m_climber2.follow(self.m_climber1, invert= True)
        self.s_climber1Encoder = self.m_climber1.getEncoder()
        self.s_climberEncoderAlt = self.m_climber1.getAlternateEncoder(8192)
        self.climbermin = -0 # find these values when built
        self.climbermax = 158 # find these values when built
        self.fullspeedmin = 10
        self.fullspeedmax = 148

    def initClimberLocks(self) -> None:

        self.p_climberlock.set(wpilib.DoubleSolenoid.Value.kForward)

        
    def setClimberSpeed(self, speed: float, override_locks: bool = False) -> None:
        '''Sets the speed of the climber motors.
        
        Args:
            speed: The speed to set the motors to, -1 to 1.
        '''
        wpilib.SmartDashboard.putString("S_Climber Pos Alt", str(self.s_climberEncoderAlt.getPosition()))
        wpilib.SmartDashboard.putString("S_Climber Pos Motor", str(self.s_climber1Encoder.getPosition()))
        if speed < 0:
            if self.s_climber1Encoder.getPosition() < self.fullspeedmin:
                speed *= 0.5
            if self.s_climber1Encoder.getPosition() < self.climbermin:
                speed = 0
                #self.p_climberlock.set(wpilib.DoubleSolenoid.Value.kForward)
        elif speed > 0:
            if self.s_climber1Encoder.getPosition() > self.fullspeedmax:
                speed *= 0.5
            if self.s_climber1Encoder.getPosition() > self.climbermax:
                speed = 0
                #self.p_climberlock.set(wpilib.DoubleSolenoid.Value.kReverse)
        
        if not override_locks:
            if speed > 0:
                self.p_climberlock.set(wpilib.DoubleSolenoid.Value.kForward)
            elif speed < 0:
                self.p_climberlock.set(wpilib.DoubleSolenoid.Value.kReverse)
            else:
                ...
            
        self.m_climber1.set(speed)
