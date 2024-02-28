import typing
import commands2
import wpilib.shuffleboard
import commands.shoulder
import commands.intake
from subsytems.shooter import Shooter
from subsytems.intake import Intake
from robot_systems import Robot, Sensors
from constants import ApriltagPositionDictBlue as apb, ApriltagPositionDictRed as apr
import config
from units.SI import degrees

class ShootNote(commands2.CommandBase):
    def __init__(
        self, 
        app: Shooter,
        speed: float,
    ) -> None:
        super().__init__()
        
        self.speed = speed
        
        self.finished = False

        self.app = app
        self.addRequirements(app)
        
    def initialize(self) -> None:
        self.app.setShooterRPM(self.speed)
        
    def execute(self) -> None:
        """Called every time the scheduler runs while the command is scheduled."""
        self.should_pos = commands.shoulder.SetShoulderAngleSpeaker(Robot.shoulder)
        self.shooter_good = self.app.setShooterRPM(self.speed)
        print("Note Excute " + str(self.should_pos)+" | "+str(self.shooter_good))
        if self.should_pos and self.shooter_good:
            if commands.intake.TransferNote(Robot.intake).isFinished():
                print("Note Shoot")
                self.finished = True

    def isFinished(self) -> bool:
        return self.finished

    def end(self, interrupted=False) -> None:
        self.app.setShooterRPM(0)
        Intake.setTransferSpeed(Robot.intake,0)
        print("Note End")

class ShooterSpeed(commands2.CommandBase):
    def __init__(
        self, 
        app: Shooter,
        speed: float,
    ) -> None:
        super().__init__()
        
        self.speed = speed
        
        self.app = app
        self.addRequirements(app)
        
    def initialize(self) -> None:
        self.at_speed = False
        #angle: degrees = self.app.calculateShoulderAngle(Sensors.odometry.getDistance(apb[7].toPose2d() if config.blue_team else apr[4].toPose2d()))
        #self.app.setShoulderAngle(angle)
        self.app.setShooterRPM(self.speed)
  
    def execute(self) -> None:
        """Called every time the scheduler runs while the command is scheduled."""
        self.at_speed = self.app.setShooterRPM(self.speed)
        # print("Shooter Running")

    def end(self, interrupted=False) -> None:
        self.app.setShooterRPM(0)
        #print("Shooter Stop")
        
class ShooterAmpSpeed(commands2.CommandBase):
    def __init__(
        self, 
        app: Shooter,
    ) -> None:
        super().__init__()
        
        self.app = app
        self.addRequirements(app)
        
    def initialize(self) -> None:
        self.at_speed = False
        #angle: degrees = self.app.calculateShoulderAngle(Sensors.odometry.getDistance(apb[7].toPose2d() if config.blue_team else apr[4].toPose2d()))
        #self.app.setShoulderAngle(angle)
        self.app.m_shooter1.set(-.2)
  
    def execute(self) -> None:
        """Called every time the scheduler runs while the command is scheduled."""
        self.app.m_shooter1.set(-.2)
        # print("Shooter Running")

    def end(self, interrupted=False) -> None:
        self.app.m_shooter1.set(0)
        #print("Shooter Stop")