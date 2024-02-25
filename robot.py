#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.

import wpilib
from wpilib import SmartDashboard, FieldObject2d
from wpilib.shuffleboard import Shuffleboard
from wpimath.geometry import Pose2d
import commands2
import typing
from ntcore import Value

from oi.OI import OI
from oi.keymap import Keymap

import autonomous
from robot_systems import Robot, Sensors
from sensors import FieldOdometry
from robotpy_toolkit_7407.sensors.limelight.limelight import LimelightController, Limelight
import commands

from constants import ApriltagPositionDictRed, ApriltagPositionDictBlue
import config

from autonomous.routines.ONE_NOTE.SL.blue import path_1

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
        
        self.tab = Shuffleboard.getTab("Match")
        
        self.field = wpilib.Field2d()
        self.field.getObject("traj").setTrajectory(path_1.trajectory)
        wpilib.SmartDashboard.putData("Field", self.field)
        
        
        OI.init() 
        
        Sensors.odometry = FieldOdometry(Robot.drivetrain, LimelightController([
            Limelight(0, 0, limelight_name="limelight-target"),
            Limelight(0, 0, limelight_name="limelight-intake"),
        ]))
        Sensors.gyro = Robot.drivetrain.gyro

        self.auto_selection = wpilib.SendableChooser()
        
        self.auto_selection.setDefaultOption("THREE NOTE BLUE", autonomous.three_note_blue)
        self.auto_selection.addOption("ONE NOTE BLUE", autonomous.one_note_blue)
        # self.auto_selection.addOption("TWO NOTE", autonomous.two_disc_red)
        
        wpilib.SmartDashboard.putData("Auto Mode", self.auto_selection)
        
        # self.auto_delay = self.tab.addNumber("Auto Delay", 0).withWidget("Number Slider").withProperties({"min": Value.makeDouble(0), "max": Value.makeDouble(15)}).getEntry()
        
        # Robot.drivetrain.reset_odometry(Robot.drivetrain.start_pose)
        for i in range(15):
            Robot.drivetrain.n_front_left.initial_zero()
            Robot.drivetrain.n_front_right.initial_zero()
            Robot.drivetrain.n_back_left.initial_zero()
            Robot.drivetrain.n_back_right.initial_zero()

    def robotPeriodic(self) -> None:
        Sensors.odometry.update()
        pose = Sensors.odometry.getPose()
        self.field.setRobotPose(pose)
        # print(Robot.drivetrain.chassis_speeds)
        SmartDashboard.putBoolean('Ready to shoot', SmartDashboard.getBoolean('Shooter at speed', False) and SmartDashboard.getBoolean('Tag Aligned', False) and SmartDashboard.getBoolean('Shoulder at angle', False))
        try:
            commands2.CommandScheduler.getInstance().run()
        except Exception as e:
            print(e)

        

    def disabledInit(self) -> None:
        """This function is called once each time the robot enters Disabled mode."""
        pass

    def disabledPeriodic(self) -> None:
        """This function is called periodically when disabled"""
        pass

    def autonomousInit(self) -> None:
        """This autonomous runs the autonomous command selected by your RobotContainer class."""
        self.alliance = wpilib.DriverStation.getAlliance()
        config.blue_team = wpilib.DriverStation.Alliance.kBlue == self.alliance
        # wait auto delay
        commands2.CommandScheduler.getInstance().schedule(commands2.WaitCommand(self.auto_delay.getDouble(0)))
        self.auto_selection.getSelected().run()

    def autonomousPeriodic(self) -> None:
        """This function is called periodically during autonomous"""
        pass

    def teleopInit(self) -> None:
        """This function is called when the robot enters operator control."""
        self.alliance = wpilib.DriverStation.getAlliance()
        config.blue_team = wpilib.DriverStation.Alliance.kBlue == self.alliance
        
         
        OI.map_controls()#Moved from robot init to avoid joystick errors if joystick not connected when robot turns on.

        commands2.CommandScheduler.getInstance().schedule(
            commands.DriveSwerveCustom(Robot.drivetrain)
        )

    def teleopPeriodic(self) -> None:
        """This function is called periodically during operator control"""
        pass

    def testInit(self) -> None:
        # Cancels all running commands at the start of test mode
        commands2.CommandScheduler.getInstance().cancelAll()
        
if __name__ == "__main__":
    wpilib.run(Robot)