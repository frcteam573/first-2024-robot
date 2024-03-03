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

from autonomous.routines.CENTERLINE.red import path_6 as path_1
#from autonomous.routines.ONE_NOTE.SL.blue import path_1

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
            # Limelight(0, 0, limelight_name="limelight-intake"),
        ]))
        Sensors.gyro = Robot.drivetrain.gyro

        self.auto_selection = wpilib.SendableChooser()
        
        self.auto_selection.setDefaultOption("FOUR NOTE BLUE", autonomous.four_note_blue)
        self.auto_selection.addOption("FOUR NOTE RED", autonomous.four_note_red)
        self.auto_selection.addOption("THREE NOTE BLUE", autonomous.three_note_blue)
        self.auto_selection.addOption("THREE NOTE RED", autonomous.three_note_red)
        self.auto_selection.addOption("TWO NOTE BLUE", autonomous.two_note_blue)
        self.auto_selection.addOption("TWO NOTE RED", autonomous.two_note_red)
        self.auto_selection.addOption("TWO NOTE CENTER BLUE", autonomous.two_note_blue_center)
        self.auto_selection.addOption("TWO NOTE CENTER RED", autonomous.two_note_red_center)
        self.auto_selection.addOption("ONE NOTE BLUE", autonomous.one_note_blue)
        self.auto_selection.addOption("ONE NOTE RED", autonomous.one_note_red)
        self.auto_selection.addOption("NOTHING BLUE", autonomous.nothing_blue)
        self.auto_selection.addOption("NOTHING RED", autonomous.nothing_red)
        self.auto_selection.addOption("CENTERLINE BLUE", autonomous.centerline_blue)
        self.auto_selection.addOption("CENTERLINE RED", autonomous.centerline_red)
        # self.auto_selection.addOption("TWO NOTE", autonomous.two_disc_red)
            
        
        self.auto_selection.onChange(lambda x: Sensors.odometry.resetOdometry(self.auto_selection.getSelected().initial_robot_pose))
        
        wpilib.SmartDashboard.putData("Auto Mode", self.auto_selection)
        wpilib.SmartDashboard.putNumber("Auto Delay",5)
        
        wpilib.SmartDashboard.putNumber("Shoulder Trim", wpilib.SmartDashboard.getNumber("Shoulder Trim", 0))
        OI.map_controls()

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
        # print('Gyro: ' +str(Sensors.odometry.getPose().rotation().radians()))
        
        
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