import typing
import commands2
import wpilib
from wpimath.geometry import Pose2d
from oi.keymap import Keymap

from subsystems import Shoulder

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
    self.in_pos=False
    self.target: Pose2d
    self.finished = False

  def initialize(self) -> None:
    """Called when the command is initially scheduled."""
    self.in_pos = False
    self.app.setShoulderLocks(False)
    #self.target = ApriltagPositionDictBlue[7].toPose2d() if config.blue_team else ApriltagPositionDictRed[4].toPose2d()
  
  def execute(self) -> bool:
    """Called every time the scheduler runs while the command is scheduled."""
    # self.target = ApriltagPositionDictBlue[7].toPose2d() if config.blue_team else ApriltagPositionDictRed[4].toPose2d() # Have to do this here so it updates if robot is moving
    distance = Sensors.odometry.getDistanceAprilTag()
    if distance:
      self.in_pos = self.app.setShoulderAngle(self.app.calculateShoulderAngle(
        distance
      ),distance)
    
    return self.in_pos  # Comment out so that the shoulder just uses PID and not locks
    

  def isFinished(self) -> bool:
    return self.finished

  def end(self, interrupted=False) -> None:
    self.app.setShoulderSpeed(0)
    self.app.setShoulderLocks(True)
    #print("Shoulder Angle Speaker END")
    
class SetShoulderAngleSpeakerAuto(commands2.CommandBase):
  def __init__(
    self, 
    app: Shoulder,
  ) -> None:
    super().__init__()

    self.app = app
    self.addRequirements(app)
    self.finished=False
    self.target: Pose2d
    self.finished = False

  def initialize(self) -> None:
    """Called when the command is initially scheduled."""
    self.finished = False
    self.target = ApriltagPositionDictBlue[7].toPose2d() if config.blue_team else ApriltagPositionDictRed[4].toPose2d() # Have to do this here so it updates if robot is moving
    self.app.setShoulderLocks(False)
    #self.target = ApriltagPositionDictBlue[7].toPose2d() if config.blue_team else ApriltagPositionDictRed[4].toPose2d()
  
  def execute(self) -> bool:
    """Called every time the scheduler runs while the command is scheduled."""
    distance = Sensors.odometry.getDistanceAprilTag()
    if not distance or distance == 0:
      distance = Sensors.odometry.getDistance(self.target)
  
    self.finished = self.app.setShoulderAngle(self.app.calculateShoulderAngle(
      distance
    ),distance)
    
  def isFinished(self) -> bool:
    return self.finished

  def end(self, interrupted=False) -> None:
    self.app.setShoulderSpeed(0)
    self.app.setShoulderLocks(True)
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
    self.finished = False
  
  def initialize(self) -> None:
    """Called when the command is initially scheduled."""
    self.app.setShoulderAngle(angle=self.angle) # find these values when built 1.7
    self.app.setShoulderLocks(False)
    
  def execute(self) -> None:
    """Called every time the scheduler runs while the command is scheduled."""
    self.app.setShoulderAngle(angle=self.angle)

    #print("Shoulder Angle: "+ str(self.angle))

  def isFinished(self) -> bool:
    return self.finished
  
  def end(self, interrupted=False) -> None:
    self.app.setShoulderSpeed(0)
    self.app.setShoulderLocks(True)
    #print("Shoulder Angle END")

class SetShoulderAngleAuto(commands2.CommandBase):
  def __init__(
    self, 
    app: Shoulder,
    angle: typing.Callable[[], float]
  ) -> None:
    super().__init__()

    self.app = app
    self.addRequirements(app)
    self.angle = angle
    self.finished = False
  
  def initialize(self) -> None:
    """Called when the command is initially scheduled."""
    self.app.setShoulderAngle(angle=self.angle) # find these values when built 1.7
    self.app.setShoulderLocks(False)
    self.finished = False
    
  def execute(self) -> None:
    """Called every time the scheduler runs while the command is scheduled."""
    if self.app.setShoulderAngle(angle=self.angle):
      self.finished = True

    #print("Shoulder Angle: "+ str(self.angle))

  def isFinished(self) -> bool:
    return self.finished
  
  def end(self, interrupted=False) -> None:
    self.app.setShoulderSpeed(0)
    self.app.setShoulderLocks(True)
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
    self.app.setShoulderLocks(False)
    
  def execute(self) -> None:
    """Called every time the scheduler runs while the command is scheduled."""
    self.app.setShoulderSpeed(-.2*Keymap.Shoulder.SHOULDER_AXIS.value)
    
  def end(self, interrupted=False) -> None:
    self.app.setShoulderSpeed(0)
    self.app.setShoulderLocks(True)

class ChangeShoulderTrim(commands2.CommandBase):
  def __init__(
    self, 
    app: Shoulder,
    trim_val: typing.Callable[[], float]
  ) -> None:
    super().__init__()

    self.app = app
    self.addRequirements(app)
    self.trim_val = trim_val
    
  
  def initialize(self) -> None:
    """Called when the command is initially scheduled."""
    self.app.changeShoulderTrim(self.trim_val)
    
    
  def execute(self) -> None:
    """Called every time the scheduler runs while the command is scheduled."""
    ...
    
  def end(self, interrupted=False) -> None:
    ...