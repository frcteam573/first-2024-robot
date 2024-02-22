import typing
import commands2
import wpilib

from subsytems.climber import Climber
        
class ClimberUp(commands2.CommandBase):
    def __init__(
        self, 
        app: Climber,
    ) -> None:
        super().__init__()

        self.app = app
        self.addRequirements(app)

    def execute(self) -> None:
        """Called every time the scheduler runs while the command is scheduled."""
        self.app.setClimberSpeed(-0.5)
        print("Climber Up")
        
    def end(self, interrupted=True) -> None:
        self.app.setClimberSpeed(0)
        print("Climber Up Stop")
        
class ClimberDown(commands2.CommandBase):
    def __init__(
        self, 
        app: Climber,
    ) -> None:
        super().__init__()

        self.app = app
        self.addRequirements(app)

    def execute(self) -> None:
        """Called every time the scheduler runs while the command is scheduled."""
        self.app.setClimberSpeed(0.9)
        print("Climber Down")
        
    def end(self, interrupted=True) -> None:
        self.app.setClimberSpeed(0)
        print("Climber Down Stop")