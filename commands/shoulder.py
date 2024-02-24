import typing
import commands2
import wpilib
from wpimath.geometry import Pose2d
from oi.keymap import Keymap

from subsytems import Shoulder

from robot_systems import Robot, Sensors

from constants import ApriltagPositionDictBlue, ApriltagPositionDictRed
import config

class SetShoulderAngleSpeaker(commands2.CommandBase):
  def __init__(
    self, 
    app: Shoulder,
  ) -> None:
    super().__init__()

    self.app = app
    self.addRequirements(app)
    
    self.target: Pose2d
    self.finished = False

  def initialize(self) -> None:
    """Called when the command is initially scheduled."""
    #self.target = ApriltagPositionDictBlue[7].toPose2d() if config.blue_team else ApriltagPositionDictRed[4].toPose2d()
  
  def execute(self) -> None:
    """Called every time the scheduler runs while the command is scheduled."""
    self.target = ApriltagPositionDictBlue[7].toPose2d() if config.blue_team else ApriltagPositionDictRed[4].toPose2d() # Have to do this here so it updates if robot is moving
    self.finished = self.app.setShoulderAngle(self.app.calculateShoulderAngle(
      Sensors.odometry.getDistanceAprilTag()
    ))
    return self.finished
    #print("Shoulder Angle Speaker")

  def isFinished(self) -> bool:
    return self.finished

  def end(self, interrupted=False) -> None:
    self.app.setShoulderSpeed(0)
    #print("Shoulder Angle Speaker END")
            
class SetShoulderAngle(commands2.CommandBase):
  def __init__(
    self, 
    app: Shoulder,
    angle: typing.Callable[[], float]
  ) -> None:
    super().__init__()

    self.app = app
    self.addRequirements(app)
    self.angle = angle
  
  def initialize(self) -> None:
    """Called when the command is initially scheduled."""
    self.finished = False
    self.app.setShoulderAngle(angle=self.angle) # find these values when built 1.7
    
  def execute(self) -> None:
    """Called every time the scheduler runs while the command is scheduled."""
    self.finished = self.app.setShoulderAngle(angle=self.angle)

    #print("Shoulder Angle: "+ str(self.angle))

  def isFinished(self) -> bool:
    return self.finished
  
  def end(self, interrupted=False) -> None:
    self.app.setShoulderSpeed(0)
    #print("Shoulder Angle END")

class JoystickMoveShoulder(commands2.CommandBase):
  def __init__(
    self, 
    app: Shoulder,
  ) -> None:
    super().__init__()

    self.app = app
    self.addRequirements(app)
    
  
  def initialize(self) -> None:
    """Called when the command is initially scheduled."""
    ...
    
  def execute(self) -> None:
    """Called every time the scheduler runs while the command is scheduled."""
    self.app.setShoulderSpeed(-0.5 * Keymap.Shoulder.SHOULDER_AXIS.value)
    
  def end(self, interrupted=False) -> None:
    self.app.setShoulderSpeed(0)