import typing
import commands2
import wpilib

from subsystems.trap import Trap
from robot_systems import Robot
        
class ExtendTrap(commands2.CommandBase):
    def __init__(
        self, 
        app: Trap,
    ) -> None:
        super().__init__()

        self.app = app
        self.addRequirements(app)
        
    def initialize(self):
        # self.app.p_climberlock.set(wpilib.DoubleSolenoid.Value.kReverse)
        ...

    def execute(self) -> None:
        """Called every time the scheduler runs while the command is scheduled."""
        self.app.ExtendTrap()
        #print("Climber Up")
        
    def end(self, interrupted=True) -> None:
        self.app.StopTrap()
        # self.app.p_climberlock.set(wpilib.DoubleSolenoid.Value.kForward)

        #print("Climber Up Stop")
        
class RetractTrap(commands2.CommandBase):
    def __init__(
        self, 
        app: Trap,
    ) -> None:
        super().__init__()

        self.app = app
        self.addRequirements(app)
        
    def initialize(self):
        # self.app.p_climberlock.set(wpilib.DoubleSolenoid.Value.kReverse)
        ...

    def execute(self) -> None:
        """Called every time the scheduler runs while the command is scheduled."""
        self.app.RetractTrap()
        #print("Climber Up")
        
    def end(self, interrupted=True) -> None:
        self.app.StopTrap()
        # self.app.p_climberlock.set(wpilib.DoubleSolenoid.Value.kForward)

        #print("Climber Up Stop")