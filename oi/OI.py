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
		Keymap.Intake.INTAKE_IN.whileTrue(commands.IntakeIn(Robot.intake))
	#	Keymap.Intake.INTAKE_IN.whileTrue(commands.ShootNote(Robot.shooter,5600))
		Keymap.Intake.INTAKE_OUT.whileTrue(commands.IntakeOut(Robot.intake))

#------------------------ Transfer -----------------------#
		commands2.button.Trigger(lambda: Keymap.Intake.TRANSFER.value > .05).whileTrue(
			commands.TransferNote(Robot.intake, True))
#------------------------ Shooter -----------------------#
		#Speaker Shooter Settings
		commands2.button.Trigger(lambda: Keymap.Intake.SHOOTER.value > .05).whileTrue(
			commands.ShooterSpeed(Robot.shooter,4000))
		
		Keymap.Intake.TRAP_HOOD.whileTrue(
			commands.ExtendTrap(Robot.trap)
		)
#------------------------ Climber -----------------------#
		Keymap.Climber.CLIMBER_UP.whileTrue(commands.ClimberJolt)
	
		Keymap.Climber.CLIMBER_DOWN.whileTrue(commands.ClimberDown(Robot.climber))

#------------------------ Shoulder -----------------------#
		commands2.button.Trigger(lambda: abs(Keymap.Shoulder.SHOULDER_AXIS.value) > .05).whileTrue(
			commands.JoystickMoveShoulder(Robot.shoulder))
		
		#Shoulder Setpoint Commands
		Keymap.Intake.FLOOR_POSITION.whileTrue(commands.SetShoulderAngle(Robot.shoulder,config.shoulder_floor_pos)) 

		Keymap.Intake.HUMAN_POSITION.whileTrue(commands.SetShoulderAngle(Robot.shoulder,config.shoulder_human_pos)) 

		Keymap.Intake.AMP_POSITION.whileTrue(commands.SetShoulderAngle(Robot.shoulder,config.shoulder_amp_pos)) 

		Keymap.Intake.TRAP_POSITION.whileTrue(commands.SetShoulderAngle(Robot.shoulder,config.shoulder_trap_pos)) 

		Keymap.Intake.SPEAKER_POSITION.whileTrue(commands.SetShoulderAngleSpeaker(Robot.shoulder))
		
		Keymap.Shoulder.SHOULDER_TRIM_UP.whileTrue(commands.ChangeShoulderTrim(Robot.shoulder,0.05))
		Keymap.Shoulder.SHOULDER_TRIM_DOWN.whileTrue(commands.ChangeShoulderTrim(Robot.shoulder,-0.05))
  
 #------------------------------- Drivetrain --------------------------------------# 
		Keymap.Drivetrain.DRIVE_STRAIGHTEN_WHEELS.onTrue(commands.DrivetrainAlignStraight(Robot.drivetrain))
  
		Keymap.Drivetrain.DRIVE_ALIGN_SPEAKER.onTrue(InstantCommand(lambda: Sensors.odometry.vision_estimator.limelights[0].change_pipeline(2)),
		# ).whileTrue(commands.SetShoulderAngleSpeaker(Robot.shoulder)
		).onFalse(InstantCommand(lambda: Sensors.odometry.vision_estimator.limelights[0].change_pipeline(0)))
	
		# Keymap.Drivetrain.DRIVE_ALIGN_AMP.whileTrue(InstantCommand(lambda: autonomous.amp_blue.run() if config.blue_team else autonomous.amp_red.run())
		# ).onFalse(InstantCommand(lambda: AutoRoutine.end()))
	
		# Keymap.Drivetrain.DRIVE_ALIGN_HUMAN.whileTrue(InstantCommand(lambda: autonomous.human_1_blue.run() if config.blue_team else autonomous.human_1_red.run())
		# ).onFalse(InstantCommand(lambda: AutoRoutine.end()))
	
		# Keymap.Drivetrain.DRIVE_ALIGN_TRAP.whileTrue(InstantCommand(lambda: autonomous.trap_1_blue.run() if config.blue_team else autonomous.trap_1_red.run())
		# ).onFalse(InstantCommand(lambda: AutoRoutine.end()))