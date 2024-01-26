#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.

import wpilib
from wpilib import SmartDashboard, FieldObject2d
from wpilib.shuffleboard import Shuffleboard
import commands2
import typing
from ntcore import Value

from oi.OI import OI
from oi.keymap import Keymap

from robot_systems import Robot, Sensors
from sensors import FieldOdometry
import commands

from constants import ApriltagPositionDictRed, ApriltagPositionDictBlue

class MyRobot(commands2.TimedCommandRobot):
    """
    Command v2 robots are encouraged to inherit from TimedCommandRobot, which
    has an implementation of robotPeriodic which runs the scheduler for you
    """

    autonomousCommand: typing.Optional[commands2.Command] = None

    def robotInit(self) -> None:
        """
        This function is run when the robot is first started up and should be used for any
        initialization code.
        """
        
        Robot.drivetrain.init()
        self.alliance = wpilib.DriverStation.getAlliance()
        
        self.field = wpilib.Field2d()
        wpilib.SmartDashboard.putData("Field", self.field)
        # self.field.getObject("traj").setTrajectory()
        
        OI.init()
        OI.map_controls()
        
        Sensors.odometry = FieldOdometry(Robot.drivetrain, None)
        Sensors.gyro = Robot.drivetrain.gyro
        
        for i in range(15):
            Robot.drivetrain.n_front_left.initial_zero()
            Robot.drivetrain.n_front_right.initial_zero()
            Robot.drivetrain.n_back_left.initial_zero()
            Robot.drivetrain.n_back_right.initial_zero()

        # Instantiate our RobotContainer.  This will perform all our button bindings, and put our
        # autonomous chooser on the dashboard.
        # self.container = RobotContainer()

    def robotPeriodic(self) -> None:
        Sensors.odometry.update()
        pose = Robot.drivetrain.odometry_estimator.getEstimatedPosition()
        self.field.setRobotPose(pose)
        self.alliance = wpilib.DriverStation.getAlliance()
        
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
        # self.autonomousCommand = self.container.getAutonomousCommand()

        # if self.autonomousCommand:
        #     self.autonomousCommand.schedule()

    def autonomousPeriodic(self) -> None:
        """This function is called periodically during autonomous"""
        pass

    def teleopInit(self) -> None:
        # This makes sure that the autonomous stops running when
        # teleop starts running. If you want the autonomous to
        # continue until interrupted by another command, remove
        # this line or comment it out.
        commands2.CommandScheduler.getInstance().schedule(
            commands.DriveSwerveCustom(Robot.drivetrain)
        )
        
        # if self.autonomousCommand:
        #     self.autonomousCommand.cancel()

    def teleopPeriodic(self) -> None:
        """This function is called periodically during operator control"""
        pass

    def testInit(self) -> None:
        # Cancels all running commands at the start of test mode
        commands2.CommandScheduler.getInstance().cancelAll()
        
if __name__ == "__main__":
    wpilib.run(Robot)