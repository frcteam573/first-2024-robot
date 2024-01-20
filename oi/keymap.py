import commands2.button
import wpilib
from robotpy_toolkit_7407.oi import (
    JoystickAxis,
    XBoxController,
)
from robotpy_toolkit_7407.oi.joysticks import Joysticks

controllerDRIVER = XBoxController
controllerOPERATOR = XBoxController
controllerNUMPAD = XBoxController


class Controllers:
    DRIVER = 0
    OPERATOR = 1
    NUMPAD = 2

    DRIVER_CONTROLLER = wpilib.Joystick(0)
    OPERATOR_CONTROLLER = wpilib.Joystick(1)
    NUMPAD_CONTROLLER = wpilib.Joystick(2)


class Keymap:
    class Intake:
        INTAKE_IN = commands2.button.JoystickButton(Controllers.DRIVER_CONTROLLER, controllerDRIVER.A)
        INTAKE_OUT = commands2.button.JoystickButton(Controllers.DRIVER_CONTROLLER, controllerDRIVER.X)
        SHOOTER = commands2.button.JoystickButton(Controllers.DRIVER_CONTROLLER, controllerDRIVER.LB)
        TRANSFER = commands2.button.JoystickButton(Controllers.DRIVER_CONTROLLER, controllerDRIVER.RB)
        
    
    class Drivetrain:
        DRIVE_X_AXIS = JoystickAxis(Controllers.DRIVER, controllerDRIVER.L_JOY[0])
        DRIVE_Y_AXIS = JoystickAxis(Controllers.DRIVER, controllerDRIVER.L_JOY[1])
        DRIVE_ROTATION_AXIS = JoystickAxis(Controllers.DRIVER, controllerDRIVER.R_JOY[0])
        DRIVE_ALIGN_NOTE = commands2.button.JoystickButton(Controllers.DRIVER_CONTROLLER, controllerDRIVER.RT)
        DRIVE_ALIGN_STRAIGHT = commands2.button.JoystickButton(Controllers.DRIVER_CONTROLLER, controllerDRIVER.START)
