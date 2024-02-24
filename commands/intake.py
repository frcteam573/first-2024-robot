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
        
    def initialize(self):
        self.finished = False

    def execute(self) -> None:
        """Called every time the scheduler runs while the command is scheduled."""
        if self.app.setIntakeSpeed(-1):
            self.finished = True
        print("Intake In")
    
    def isFinished(self) -> bool:
        return self.finished
        
    def end(self, interrupted=False) -> None:
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
        #print("Intake Out")
        
    def end(self, interrupted=False) -> None:
        self.app.setIntakeSpeed(0)
        #print("Intake Out End")
        
class TransferNote(commands2.CommandBase):
    def __init__(
        self, 
        app: Intake,
    ) -> None:
        super().__init__()

        self.app = app
        self.addRequirements(app)
        
    def initialize(self):
        self.finished = False

    def execute(self) -> None:
        """Called every time the scheduler runs while the command is scheduled."""
        if self.app.setTransferSpeed(1):
            self.finished = True

    def isFinished(self) -> bool:
        return self.finished
        
    def end(self, interrupted=False) -> None:
        self.app.setTransferSpeed(0)
        #print("Transfer End")