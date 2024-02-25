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
        self.climbermin = -100000 # find these values when built
        self.climbermax = 1000000 # find these values when built

        
    def setClimberSpeed(self, speed: float) -> None:
        '''Sets the speed of the climber motors.
        
        Args:
            speed: The speed to set the motors to, -1 to 1.
        '''
        wpilib.SmartDashboard.putString("S_Climber Pos Alt", str(self.s_climberEncoderAlt.getPosition()))
        wpilib.SmartDashboard.putString("S_Climber Pos Motor", str(self.s_climber1Encoder.getPosition()))
        if self.s_climber1Encoder.getPosition() < self.climbermin and speed < 0:
            self.m_climber1.set(0)
            self.p_climberlock.set(wpilib.DoubleSolenoid.Value.kForward)
        elif self.s_climber1Encoder.getPosition() > self.climbermax and speed > 0:
            self.m_climber1.set(0)
            self.p_climberlock.set(wpilib.DoubleSolenoid.Value.kForward)
        else:
            self.m_climber1.set(speed)
            if speed < 0:
                self.p_climberlock.set(wpilib.DoubleSolenoid.Value.kReverse)
            else:
                self.p_climberlock.set(wpilib.DoubleSolenoid.Value.kForward)
