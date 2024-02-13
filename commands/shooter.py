import typing
import commands2
import wpilib.shuffleboard

from subsytems.appendage import Appendage

class ShooterActivate(commands2.CommandBase):
    def __init__(
        self, 
        app: Appendage,
        speed: float,
    ) -> None:
        super().__init__()
        
        self.speed = speed

        self.app = app
        self.addRequirements(app)

    def execute(self) -> None:
        """Called every time the scheduler runs while the command is scheduled."""
        self.app.setShooter(-self.speed)
        print("shooter velocity:", self.app.s_shooterEncoder1.getVelocity())
        
    
        
    def end(self, interrupted=False) -> None:
        self.app.setShooter(0)