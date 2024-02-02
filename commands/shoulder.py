import typing
import commands2
import wpilib
from wpimath.geometry import Pose2d

from subsytems import Appendage

from robot_systems import Robot, Sensors

from constants import ApriltagPositionDictBlue, ApriltagPositionDictRed
import config

class SetShoulderAngleSpeaker(commands2.CommandBase):
  def __init__(
    self, 
    app: Appendage,
  ) -> None:
    super().__init__()

    self.app = app
    self.addRequirements(app)
    
    self.target: Pose2d

  def initialize(self) -> None:
    """Called when the command is initially scheduled."""
    self.target = ApriltagPositionDictBlue[7].toPose2d() if config.blue_team else ApriltagPositionDictRed[4].toPose2d()
  
  def execute(self) -> None:
    """Called every time the scheduler runs while the command is scheduled."""
    self.app.setShoulderAngle(self.app.calculateShoulderAngle(
      Sensors.odometry.getDistance(self.target)
    ))

  def end(self, interrupted=False) -> None:
    ...
            
class SetShoulderAngleFloor(commands2.CommandBase):
  def __init__(
    self, 
    app: Appendage,
  ) -> None:
    super().__init__()

    self.app = app
    self.addRequirements(app)
  
  def initialize(self) -> None:
    """Called when the command is initially scheduled."""
    self.app.setShoulderAngle(0) # find these values when built
    
  def execute(self) -> None:
    """Called every time the scheduler runs while the command is scheduled."""
    ...
    
  def end(self, interrupted=False) -> None:
    ...

class SetShoulderAngleAmp(commands2.CommandBase):
  def __init__(
    self, 
    app: Appendage,
  ) -> None:
    super().__init__()

    self.app = app
    self.addRequirements(app)
  
  def initialize(self) -> None:
    """Called when the command is initially scheduled."""
    self.app.setShoulderAngle(0) # find these values when built
    
  def execute(self) -> None:
    """Called every time the scheduler runs while the command is scheduled."""
    ...
    
  def end(self, interrupted=False) -> None:
    ...
    
class SetShoulderAngleHuman(commands2.CommandBase):
  def __init__(
    self, 
    app: Appendage,
  ) -> None:
    super().__init__()

    self.app = app
    self.addRequirements(app)
  
  def initialize(self) -> None:
    """Called when the command is initially scheduled."""
    self.app.setShoulderAngle(0) # find these values when built
    
  def execute(self) -> None:
    """Called every time the scheduler runs while the command is scheduled."""
    ...
    
  def end(self, interrupted=False) -> None:
    ...
    
class SetShoulderAngleTrap(commands2.CommandBase):
  def __init__(
    self, 
    app: Appendage,
  ) -> None:
    super().__init__()

    self.app = app
    self.addRequirements(app)
  
  def initialize(self) -> None:
    """Called when the command is initially scheduled."""
    self.app.setShoulderAngle(0) # find these values when built
    
  def execute(self) -> None:
    """Called every time the scheduler runs while the command is scheduled."""
    ...
    
  def end(self, interrupted=False) -> None:
    ...