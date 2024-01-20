import typing
import commands2
import wpilib

from subsytems.appendage import Appendage

class Intake(commands2.CommandBase):
    def __init__(
        self, 
        app: Appendage,
        speed: typing.Callable[[], float],
    ) -> None:
        super().__init__()
        
        self.speed = speed

        self.app = app
        self.addRequirements(app)

    def execute(self) -> None:
        """Called every time the scheduler runs while the command is scheduled."""
        self.app.setIntake(self.speed())
        
    def end(self, interrupted=False) -> None:
        self.app.setIntake(0)
        
class IntakeIn(commands2.CommandBase):
    def __init__(
        self, 
        app: Appendage,
    ) -> None:
        super().__init__()

        self.app = app
        self.addRequirements(app)

    def execute(self) -> None:
        """Called every time the scheduler runs while the command is scheduled."""
        self.app.setIntake(-.5)
        
    def end(self, interrupted=False) -> None:
        self.app.setIntake(0)
        
class IntakeOut(commands2.CommandBase):
    def __init__(
        self, 
        app: Appendage,
    ) -> None:
        super().__init__()

        self.app = app
        self.addRequirements(app)

    def execute(self) -> None:
        """Called every time the scheduler runs while the command is scheduled."""
        self.app.setIntake(.5)
        
    def end(self, interrupted=False) -> None:
        self.app.setIntake(0)
        
class TransferNote(commands2.CommandBase):
    def __init__(
        self, 
        app: Appendage,
    ) -> None:
        super().__init__()

        self.app = app
        self.addRequirements(app)

    def execute(self) -> None:
        """Called every time the scheduler runs while the command is scheduled."""
        self.app.setTransfer(1)
        
    def end(self, interrupted=False) -> None:
        self.app.setTransfer(0)