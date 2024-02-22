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
        self.app.setIntakeSpeed(self.speed())
        
    def end(self, interrupted=False) -> None:
        self.app.setIntakeSpeed(0)
        
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
        if not self.app.s_claw_lightgate.get(): #test value
            self.app.setIntakeSpeed(0)
        else:
            self.app.setIntakeSpeed(-1)
        #print("Excute")
        
    def end(self, interrupted=True) -> None:
        self.app.setIntakeSpeed(0)
        #print("end")
        
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
        self.app.setIntakeSpeed(1)
        
    def end(self, interrupted=False) -> None:
        self.app.setIntakeSpeed(0)
        
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
        self.app.setTransfer(.7)
        
    def end(self, interrupted=False) -> None:
        self.app.setTransfer(0)