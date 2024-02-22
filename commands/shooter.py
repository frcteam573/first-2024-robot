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
        self.shouldpos = commands.shoulder.SetShoulderAngleSpeaker(Robot.shoulder).isFinished()
        self.shootergood = self.app.setShooterRPM(self.speed)
        #print("Note Excute " + str(self.shouldpos)+"| "+str(self.shootergood))
        if self.shouldpos and self.shootergood:
            commands.intake.TransferNote(Robot.intake)
            commands2.ScheduleCommand(commands2.WaitCommand(.5))
            #print("Note Shoot")
            self.finished = True

    def isFinished(self) -> bool:
        return self.finished

    def end(self, interrupted=False) -> None:
        self.app.setShooterRPM(0)
        Intake.setTransferSpeed(Robot.intake,0)
        #print("Note End")

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
        
        #angle: degrees = self.app.calculateShoulderAngle(Sensors.odometry.getDistance(apb[7].toPose2d() if config.blue_team else apr[4].toPose2d()))
        #self.app.setShoulderAngle(angle)
        self.app.setShooterRPM(self.speed)
  
    def execute(self) -> None:
        """Called every time the scheduler runs while the command is scheduled."""
        self.Atspeed = self.app.setShooterRPM(self.speed)
        #print("Shooter Running")
        return self.Atspeed


    def end(self, interrupted=False) -> None:
        self.app.setShooterRPM(0)
        #print("Shooter Stop")