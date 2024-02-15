import typing
import commands2
import wpilib.shuffleboard

from subsytems.appendage import Appendage
from robot_systems import Robot, Sensors
from constants import ApriltagPositionDictBlue as apb, ApriltagPositionDictRed as apr
import config
from units.SI import degrees

class ShootNote(commands2.CommandBase):
    def __init__(
        self, 
        app: Appendage,
        speed: float,
    ) -> None:
        super().__init__()
        
        self.speed = speed
        
        self.finished = False

        self.app = app
        self.addRequirements(app)
        
    def initialize(self) -> None:
        self.app.setTransferSpeed(0)
        angle: degrees = self.app.calculateShoulderAngle(Sensors.odometry.getDistance(apb[7].toPose2d() if config.blue_team else apr[4].toPose2d()))
        self.app.setShoulderAngle(angle)
        self.app.setShooterRPM(self.speed)

    def execute(self) -> None:
        """Called every time the scheduler runs while the command is scheduled."""
        if 1.05 > self.app.s_shooterEncoder1.getVelocity() / self.speed > .95 and self.speed != 0:
            self.app.setTransferSpeed(1)
            commands2.ScheduleCommand(commands2.WaitCommand(.5))
            self.finished = True

    def isFinished(self) -> bool:
        return self.finished

    def end(self, interrupted=False) -> None:
        self.app.setShooter(0)
        self.app.setTransferSpeed(0)