import typing
import commands2
import wpilib

from subsytems.intake import Intake

class Intake(commands2.CommandBase):
    def __init__(
        self, 
        app: Intake,
        speed: typing.Callable[[], float],
    ) -> None:
        super().__init__()
        
        self.speed = speed

        self.app = app
        self.addRequirements(app)

    def execute(self) -> None:
        """Called every time the scheduler runs while the command is scheduled."""
        self.app.setIntakeSpeed(self.speed())
        
    def end(self, interrupted=False) -> None:
        self.app.setIntakeSpeed(0)
        
class IntakeIn(commands2.CommandBase):
    def __init__(
        self, 
        app: Intake,
    ) -> None:
        super().__init__()

        self.app = app
        self.addRequirements(app)

    def execute(self) -> None:
        """Called every time the scheduler runs while the command is scheduled."""
        if not self.app.s_claw_lightgate.get(): #test value
            self.app.setIntakeSpeed(0)
        else:
            self.app.setIntakeSpeed(-1)
        print("Intake In")
        
    def end(self, interrupted=True) -> None:
        self.app.setIntakeSpeed(0)
        print("Intake In End")
        
class IntakeOut(commands2.CommandBase):
    def __init__(
        self, 
        app: Intake,
    ) -> None:
        super().__init__()

        self.app = app
        self.addRequirements(app)

    def execute(self) -> None:
        """Called every time the scheduler runs while the command is scheduled."""
        self.app.setIntakeSpeed(1)
        print("Intake Out")
        
    def end(self, interrupted=False) -> None:
        self.app.setIntakeSpeed(0)
        print("Intake Out End")
        
class TransferNote(commands2.CommandBase):
    def __init__(
        self, 
        app: Intake,
    ) -> None:
        super().__init__()

        self.app = app
        self.addRequirements(app)

    def execute(self) -> None:
        """Called every time the scheduler runs while the command is scheduled."""
        self.app.setTransferSpeed(1)
        print("Transfer Note")
        
    def end(self, interrupted=False) -> None:
        self.app.setTransferSpeed(0)
        print("Transfer End")