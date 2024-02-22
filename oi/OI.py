import math

import commands2
import wpilib
from commands2 import (
	InstantCommand,
	ParallelCommandGroup,
	SequentialCommandGroup,
	WaitCommand,
)
from robotpy_toolkit_7407.utils import logger

import commands
import autonomous
from autonomous.auto_routine import AutoRoutine
import config
from oi.keymap import Controllers, Keymap
from robot_systems import Robot, Sensors

logger.info("Hi, I'm OI!")

class OI:
	@staticmethod
	def init() -> None:
		pass

	@staticmethod
	def map_controls():
		logger.info("Mapping controls...")

#------------------------ Intake -----------------------#
		Keymap.Intake.INTAKE_IN.whileTrue(command=commands.IntakeIn(Robot.appendage))
		Keymap.Intake.INTAKE_OUT.whileTrue(command=commands.IntakeOut(Robot.appendage))
		# Keymap.Intake.INTAKE_IN.onTrue(
		# 	InstantCommand(lambda: Robot.appendage.setIntakeSpeed(-1))
		# ).onFalse(command=commands.IntakeIn(Robot.appendage).end(True)
		# )
		# Keymap.Intake.INTAKE_OUT.onTrue(	# We should consider added a variable which means climber deployed or not, then we can adjust speed out for trap scoring.
		# 	InstantCommand(lambda: Robot.appendage.setIntakeSpeed(1))
		# ).onFalse(
		# 	InstantCommand(lambda: Robot.appendage.setIntakeSpeed(0))
		# )
#------------------------ Transfer -----------------------#
		commands2.button.Trigger(lambda: Keymap.Intake.TRANSFER.value > .05).whileTrue(
			InstantCommand(lambda: Robot.appendage.setTransferSpeed(1))
		).onFalse(
			InstantCommand(lambda: Robot.appendage.setTransferSpeed(0))
		)
#------------------------ Shooter -----------------------#
		#Speaker Shooter Settings
		Keymap.Intake.SHOOTER_AMP.whileTrue(
			command=commands.ShooterSpeed(Robot.appendage,5600)
		)
		# commands2.button.Trigger(Keymap.Intake.SHOOTER.value > .05).whileTrue(
		# 	command=commands.ShooterSpeed(Robot.appendage)
		# )

		# Amp Shooter Settings
		# Keymap.Intake.SHOOTER_AMP.onTrue(
		# 	InstantCommand(lambda: Robot.appendage.setShooterRPM(1000))
		# ).onFalse(
		# 	InstantCommand(lambda: Robot.appendage.setShooterRPM(0))
		# )
#------------------------ Climber -----------------------#
		Keymap.Climber.CLIMBER_UP.whileTrue(
			InstantCommand(lambda: Robot.appendage.setClimberSpeed(-0.5))
		).onFalse(
			InstantCommand(lambda: Robot.appendage.setClimberSpeed(0))
		)
		Keymap.Climber.CLIMBER_DOWN.whileTrue(
			InstantCommand(lambda: Robot.appendage.setClimberSpeed(0.9))
		).onFalse(
			InstantCommand(lambda: Robot.appendage.setClimberSpeed(0))
		)
#------------------------ Shoulder -----------------------#
		commands2.button.Trigger(lambda: math.fabs(Keymap.Shoulder.SHOULDER_AXIS.value) > .1).whileTrue(
			InstantCommand(lambda: Robot.appendage.setShoulderSpeed(Keymap.Shoulder.SHOULDER_AXIS.value))
		).onFalse(
			InstantCommand(lambda: Robot.appendage.setShoulderSpeed(0))
		)
		
		#Shoulder Setpoint Commands
		Keymap.Intake.FLOOR_POSITION.whileTrue(command=commands.SetShoulderAngle(Robot.appendage,config.Shoulder_Floor_Pos)) 

		Keymap.Intake.HUMAN_POSITION.whileTrue(command=commands.SetShoulderAngle(Robot.appendage,config.Shoulder_Human_Pos)) 

		Keymap.Intake.AMP_POSITION.whileTrue(command=commands.SetShoulderAngle(Robot.appendage,config.Shoulder_Amp_Pos)) 

		#Keymap.Intake.TRAP_POSITION.whileTrue(command=commands.SetShoulderAngle(Robot.appendage,config.Shoulder_Trap_Pos)) 

		Keymap.Intake.SPEAKER_POSITION.whileTrue(command=commands.SetShoulderAngleSpeaker(Robot.appendage)) 

 #------------------------------- Drivetrain --------------------------------------# 
		Keymap.Drivetrain.DRIVE_STRAIGHTEN_WHEELS.onTrue(commands.DrivetrainAlignStraight(Robot.drivetrain))
		
		Keymap.Drivetrain.DRIVE_ALIGN_NOTE.onTrue(InstantCommand(lambda: Sensors.odometry.vision_estimator.limelights[0].change_pipeline(1)),
		).onFalse(InstantCommand(lambda: Sensors.odometry.vision_estimator.limelights[0].change_pipeline(0)))
  
		Keymap.Drivetrain.DRIVE_ALIGN_SPEAKER.onTrue(InstantCommand(lambda: Sensors.odometry.vision_estimator.limelights[0].change_pipeline(2)),
		# ).whileTrue(commands.SetShoulderAngleSpeaker(Robot.appendage)
		).onFalse(InstantCommand(lambda: Sensors.odometry.vision_estimator.limelights[0].change_pipeline(0)))
	
		Keymap.Drivetrain.DRIVE_ALIGN_AMP.whileTrue(InstantCommand(lambda: autonomous.amp_blue.run() if config.blue_team else autonomous.amp_red.run())
		).onFalse(InstantCommand(lambda: AutoRoutine.end()))
	
		Keymap.Drivetrain.DRIVE_ALIGN_HUMAN.whileTrue(InstantCommand(lambda: autonomous.human_1_blue.run() if config.blue_team else autonomous.human_1_red.run())
		).onFalse(InstantCommand(lambda: AutoRoutine.end()))
	
		Keymap.Drivetrain.DRIVE_ALIGN_TRAP.whileTrue(InstantCommand(lambda: autonomous.trap_1_blue.run() if config.blue_team else autonomous.trap_1_red.run())
		).onFalse(InstantCommand(lambda: AutoRoutine.end()))