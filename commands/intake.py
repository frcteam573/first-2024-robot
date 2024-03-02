import typing
import commands2
import wpilib
from oi.keymap import Keymap

from subsytems.intake import Intake

class IntakeSpeed(commands2.CommandBase):
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
        
    def initialize(self) -> None:
        self.finished = False

    def execute(self) -> None:
        """Called every time the scheduler runs while the command is scheduled."""
        if self.app.setIntakeSpeed(-1):
            self.finished = True
        #print("Intake In")
    
    def isFinished(self) -> bool:
        return self.finished
        
    def end(self, interrupted=False) -> None:
        self.app.setIntakeSpeed(0)
        #print("Intake In End")
        
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
        self.app.setIntakeSpeed(.3 if Keymap.Intake.TRAP_POSITION.getAsBoolean() else 1)
        # self.app.setIntakeSpeed(.3)
        #print("Intake Out")
        
    def end(self, interrupted=False) -> None:
        self.app.setIntakeSpeed(0)
        #print("Intake Out End")
        
class TransferNote(commands2.CommandBase):
    def __init__(
        self, 
        app: Intake,
        overide: bool = False
    ) -> None:
        super().__init__()

        self.app = app
        self.addRequirements(app)

        self.overide = overide

    def initialize(self) -> None:
        self.finished = False

    def execute(self) -> None:
        """Called every time the scheduler runs while the command is scheduled."""
        #print("Transfer")
        if self.app.setTransferSpeed(1, self.overide):
            self.finished = True
            
    def isFinished(self) -> bool:
        return self.finished
        
    def end(self, interrupted=False) -> None:
        self.app.setTransferSpeed(0)
        #print("Transfer End")