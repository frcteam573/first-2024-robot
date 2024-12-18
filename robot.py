#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.

import wpilib
from wpilib import SmartDashboard, FieldObject2d
from wpilib.shuffleboard import Shuffleboard, BuiltInWidgets
from wpimath.geometry import Pose2d
import commands2
from cscore import CameraServer
import typing
from ntcore import Value

from oi.OI import OI
from oi.keymap import Keymap

import autonomous
from robot_systems import Robot, Sensors
from sensors import FieldOdometry
from robotpy_toolkit_7407.sensors.limelight.limelight import LimelightController, Limelight
import commands

import config

# from autonomous.routines.ONE_NOTE.SL.blue import path_1

class MyRobot(commands2.TimedCommandRobot):
    """
    Command v2 robots are encouraged to inherit from TimedCommandRobot, which
    has an implementation of robotPeriodic which runs the scheduler for you
    """

    def robotInit(self) -> None:
        """
        This function is run when the robot is first started up and should be used for any
        initialization code.
        """
        
        Robot.drivetrain.init()
        Robot.drivetrain.reset_odometry(Robot.drivetrain.start_pose)
        self.alliance = wpilib.DriverStation.getAlliance()
        config.blue_team = wpilib.DriverStation.Alliance.kBlue == self.alliance
        
        # self.power = Shuffleboard.getTab("Power Consumption")
        # self.PDP = wpilib.PowerDistribution(20, wpilib.PowerDistribution.ModuleType.kRev)
        # self.intake_power = self.power.add("Intake", self.PDP.getCurrent(4)).withWidget(BuiltInWidgets.kGraph).getEntry()
        # self.transfer_power = self.power.add("Transfer", self.PDP.getCurrent(5)).withWidget(BuiltInWidgets.kGraph).getEntry()
        # self.shooter1_power = self.power.add("Shooter 1", self.PDP.getCurrent(3)).withWidget(BuiltInWidgets.kGraph).getEntry()
        # self.shooter2_power = self.power.add("Shooter 2", self.PDP.getCurrent(2)).withWidget(BuiltInWidgets.kGraph).getEntry()
        # self.swerve_bld_power = self.power.add("BL Drive", self.PDP.getCurrent(13)).withWidget(BuiltInWidgets.kGraph).getEntry()
        # self.swerve_bls_power = self.power.add("BL Spin", self.PDP.getCurrent(14)).withWidget(BuiltInWidgets.kGraph).getEntry()
        # self.swerve_brd_power = self.power.add("BR Drive", self.PDP.getCurrent(8)).withWidget(BuiltInWidgets.kGraph).getEntry()
        # self.swerve_brs_power = self.power.add("BR Spin", self.PDP.getCurrent(9)).withWidget(BuiltInWidgets.kGraph).getEntry()
        # self.swerve_fld_power = self.power.add("FL Drive", self.PDP.getCurrent(18)).withWidget(BuiltInWidgets.kGraph).getEntry()
        # self.swerve_fls_power = self.power.add("FL Spin", self.PDP.getCurrent(17)).withWidget(BuiltInWidgets.kGraph).getEntry()
        # self.swerve_frd_power = self.power.add("FR Drive", self.PDP.getCurrent(0)).withWidget(BuiltInWidgets.kGraph).getEntry()
        # self.swerve_frs_power = self.power.add("FR Spin", self.PDP.getCurrent(1)).withWidget(BuiltInWidgets.kGraph).getEntry()
        # self.shoulder1_power = self.power.add("Shoulder 1", self.PDP.getCurrent(6)).withWidget(BuiltInWidgets.kGraph).getEntry()
        # self.shoulder2_power = self.power.add("Shoulder 2", self.PDP.getCurrent(15)).withWidget(BuiltInWidgets.kGraph).getEntry()
        # self.elevator1_power = self.power.add("Elevator 1", self.PDP.getCurrent(7)).withWidget(BuiltInWidgets.kGraph).getEntry()
        # self.elevator2_power = self.power.add("Elevator 2", self.PDP.getCurrent(16)).withWidget(BuiltInWidgets.kGraph).getEntry()
        # self.pcm_power = self.power.add("PCM (Compressor)", self.PDP.getCurrent(22)).withWidget(BuiltInWidgets.kGraph).getEntry()
        
        self.field = wpilib.Field2d()
        # self.field.getObject("traj").setTrajectory(path_1.trajectory)
        wpilib.SmartDashboard.putData("Field", self.field)
        
        CameraServer.startAutomaticCapture() # automatically puts usb camera to SmartDashboard
        
        OI.init() 
        
        Sensors.odometry = FieldOdometry(Robot.drivetrain, LimelightController([
            Limelight(0, 0, limelight_name="limelight-target"),
            # Limelight(0, 0, limelight_name="limelight-intake"),
        ]))
        Sensors.gyro = Robot.drivetrain.gyro

        self.auto_selection = wpilib.SendableChooser()
        # if config.blue_team:
        self.auto_selection.setDefaultOption("FOUR NOTE BLUE", autonomous.four_note_blue)
        self.auto_selection.addOption("THREE NOTE M 1 2 BLUE", autonomous.three_note_middle_1_2_blue)
        self.auto_selection.addOption("THREE NOTE M 2 3 BLUE", autonomous.three_note_middle_2_3_blue)
        self.auto_selection.addOption("TWO NOTE TOP BLUE", autonomous.two_note_top_blue)
        self.auto_selection.addOption("TWO NOTE MIDDLE BLUE", autonomous.two_note_middle_blue)
        self.auto_selection.addOption("TWO NOTE BOTTOM BLUE", autonomous.two_note_bottom_center_blue)
        self.auto_selection.addOption("ONE NOTE SIDE BLUE", autonomous.one_note_side_blue)
        self.auto_selection.addOption("ONE NOTE TOP BLUE", autonomous.one_note_top_blue)
        self.auto_selection.addOption("ONE NOTE MIDDLE BLUE", autonomous.one_note_middle_blue)
        self.auto_selection.addOption("ONE NOTE BOTTOM BLUE", autonomous.one_note_bottom_blue)
        self.auto_selection.addOption("NOTHING BLUE", autonomous.nothing_blue)
        self.auto_selection.addOption("CENTERLINE BLUE", autonomous.centerline_blue)
    # else:
        self.auto_selection.setDefaultOption("FOUR NOTE RED", autonomous.four_note_red)
        self.auto_selection.addOption("THREE NOTE M 1 2 RED", autonomous.three_note_middle_1_2_red)
        self.auto_selection.addOption("THREE NOTE M 2 3 RED", autonomous.three_note_middle_2_3_red)
        self.auto_selection.addOption("TWO NOTE TOP RED", autonomous.two_note_top_red)
        self.auto_selection.addOption("TWO NOTE MIDDLE RED", autonomous.two_note_middle_red)
        self.auto_selection.addOption("TWO NOTE BOTTOM RED", autonomous.two_note_bottom_center_red)
        self.auto_selection.addOption("ONE NOTE SIDE RED", autonomous.one_note_side_red)
        self.auto_selection.addOption("ONE NOTE TOP RED", autonomous.one_note_top_red)
        self.auto_selection.addOption("ONE NOTE MIDDLE RED", autonomous.one_note_middle_red)
        self.auto_selection.addOption("ONE NOTE BOTTOM RED", autonomous.one_note_bottom_red)
        self.auto_selection.addOption("NOTHING RED", autonomous.nothing_red)
        self.auto_selection.addOption("CENTERLINE RED", autonomous.centerline_red)
            
        
        # self.auto_selection.onChange(lambda x: Sensors.odometry.resetOdometry(self.auto_selection.getSelected().initial_robot_pose))
        
        wpilib.SmartDashboard.putData("Auto Mode", self.auto_selection)
        wpilib.SmartDashboard.putNumber("Auto Delay",5)
        
        wpilib.SmartDashboard.putNumber("Shoulder Trim", wpilib.SmartDashboard.getNumber("Shoulder Trim", 0))
        OI.map_controls()
        Robot.climber.initClimberLocks()
        Robot.trap.StopTrap()

        # Robot.drivetrain.reset_odometry(Robot.drivetrain.start_pose)
        for i in range(15):
            Robot.drivetrain.n_front_left.initial_zero()
            Robot.drivetrain.n_front_right.initial_zero()
            Robot.drivetrain.n_back_left.initial_zero()
            Robot.drivetrain.n_back_right.initial_zero()

    def robotPeriodic(self) -> None:
        Sensors.odometry.update()
        SmartDashboard.putNumber("Gyro angle", Robot.drivetrain.gyro.get_robot_heading())
        pose = Sensors.odometry.getPose()
        self.field.setRobotPose(pose)
        # print(Robot.drivetrain.chassis_speeds)
        # print('Gyro: ' +str(Sensors.odometry.getPose().rotation().radians()))
        
        # print(Robot.drivetrain.n_front_left.m_turn.encoder.getPosition())
        
        # Power consumption
        # self.intake_power.setDouble(self.PDP.getCurrent(4))
        # self.transfer_power.setDouble(self.PDP.getCurrent(5))
        # self.shooter1_power.setDouble(self.PDP.getCurrent(3))
        # self.shooter2_power.setDouble(self.PDP.getCurrent(2))
        # self.swerve_bld_power.setDouble(self.PDP.getCurrent(13))
        # self.swerve_bls_power.setDouble(self.PDP.getCurrent(14))
        # self.swerve_brd_power.setDouble(self.PDP.getCurrent(8))
        # self.swerve_brs_power.setDouble(self.PDP.getCurrent(9))
        # self.swerve_fld_power.setDouble(self.PDP.getCurrent(18))
        # self.swerve_fls_power.setDouble(self.PDP.getCurrent(17))
        # self.swerve_frd_power.setDouble(self.PDP.getCurrent(0))
        # self.swerve_frs_power.setDouble(self.PDP.getCurrent(1))
        # self.shoulder1_power.setDouble(self.PDP.getCurrent(6))
        # self.shoulder2_power.setDouble(self.PDP.getCurrent(15))
        # self.elevator1_power.setDouble(self.PDP.getCurrent(7))
        # self.elevator2_power.setDouble(self.PDP.getCurrent(16))
        # self.pcm_power.setDouble(self.PDP.getCurrent(22))
        
        

        SmartDashboard.putBoolean('Ready to shoot', SmartDashboard.getBoolean('Shooter at speed', False) and SmartDashboard.getBoolean('Tag aligned', False) and SmartDashboard.getBoolean('Shoulder at angle', False))
        if SmartDashboard.getBoolean('Ready to shoot', False):
            Robot.led.setGreenLed()
        elif SmartDashboard.getBoolean("Note in", False):
            Robot.led.setOrangeLed()
        else:
            Robot.led.setBlackLed()
        try:
            commands2.CommandScheduler.getInstance().run()
        except Exception as e:
            print(e)

        

    def disabledInit(self) -> None:
        """This function is called once each time the robot enters Disabled mode."""

    def disabledPeriodic(self) -> None:
        """This function is called periodically when disabled"""
        pass

    def autonomousInit(self) -> None:
        """This autonomous runs the autonomous command selected by your RobotContainer class."""
        for i in range(15):
            Robot.drivetrain.n_front_left.initial_zero()
            Robot.drivetrain.n_front_right.initial_zero()
            Robot.drivetrain.n_back_left.initial_zero()
            Robot.drivetrain.n_back_right.initial_zero()
        
        self.alliance = wpilib.DriverStation.getAlliance()
        config.blue_team = wpilib.DriverStation.Alliance.kBlue == self.alliance
        self.auto_selection.getSelected().run()
        

    def autonomousPeriodic(self) -> None:
        """This function is called periodically during autonomous"""
        pass

    def teleopInit(self) -> None:
        """This function is called when the robot enters operator control."""
        self.alliance = wpilib.DriverStation.getAlliance()
        config.blue_team = wpilib.DriverStation.Alliance.kBlue == self.alliance
        
        commands2.CommandScheduler.getInstance().schedule(
            commands.DriveSwerveCustom(Robot.drivetrain)
        )

    def teleopPeriodic(self) -> None:
        """This function is called periodically during operator control"""
        # wpilib.SmartDashboard.putNumber("distance", Sensors.odometry.getDistanceAprilTag())

    def testInit(self) -> None:
        # Cancels all running commands at the start of test mode
        commands2.CommandScheduler.getInstance().cancelAll()
        
if __name__ == "__main__":
    wpilib.run(Robot)