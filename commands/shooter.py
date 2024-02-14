import typing
import commands2
import wpilib.shuffleboard

from subsytems.appendage import Appendage

class ShootNote(commands2.CommandBase):
    def __init__(
        self, 
        app: Appendage,
        speed: float,
        angle: float,
    ) -> None:
        super().__init__()
        
        self.speed = speed
        self.angle = angle

        self.app = app
        self.addRequirements(app)
        
    def initialize(self) -> None:
        # calculate shoulder angle
        # set shoulder angle PID reference
        # set shooter RPM to 11000
        ...

    def execute(self) -> None:
        """Called every time the scheduler runs while the command is scheduled."""
        if 1.05 > self.app.s_shooterEncoder1.getVelocity() / self.speed > .95 and self.speed != 0:
            self.app.setTransferSpeed(1)
            # wait .5 seconds
        else:
            self.app.setTransferSpeed(0)

    def end(self, interrupted=False) -> None:
        self.app.setShooter(0)
        self.app.setTransferSpeed(0)