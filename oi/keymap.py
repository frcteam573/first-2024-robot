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
        INTAKE_IN = commands2.button.JoystickButton(Controllers.OPERATOR_CONTROLLER, controllerDRIVER.LB)
        INTAKE_OUT = commands2.button.JoystickButton(Controllers.OPERATOR_CONTROLLER, controllerDRIVER.RB)
        SHOOTER = JoystickAxis(Controllers.OPERATOR, controllerDRIVER.RT)
        TRANSFER = commands2.button.JoystickButton(Controllers.OPERATOR_CONTROLLER, controllerDRIVER.RB)
        
        FLOOR_POSITION = commands2.button.JoystickButton(Controllers.OPERATOR_CONTROLLER, controllerDRIVER.A)
        SPEAKER_POSITION = commands2.button.JoystickButton(Controllers.OPERATOR_CONTROLLER, controllerDRIVER.Y)
        HUMAN_POSITION = commands2.button.JoystickButton(Controllers.OPERATOR_CONTROLLER, controllerDRIVER.B)
        AMP_POSITION = commands2.button.JoystickButton(Controllers.OPERATOR_CONTROLLER, controllerDRIVER.X)
        TRAP_POSITION = commands2.button.JoystickButton(Controllers.OPERATOR_CONTROLLER, controllerDRIVER.SELECT)
        
    class Climber:
        CLIMBER_UP = commands2.button.JoystickButton(Controllers.DRIVER_CONTROLLER, controllerDRIVER.RB)
        CLIMBER_DOWN = commands2.button.JoystickButton(Controllers.DRIVER_CONTROLLER, controllerDRIVER.LB)
        
    class Shoulder:
        SHOULDER_AXIS = JoystickAxis(Controllers.OPERATOR, controllerDRIVER.L_JOY[0])
    
    class Drivetrain:
        DRIVE_STRAIGHTEN_WHEELS = commands2.button.JoystickButton(Controllers.DRIVER_CONTROLLER, controllerDRIVER.SELECT)
        
        DRIVE_X_AXIS = JoystickAxis(Controllers.DRIVER, controllerDRIVER.L_JOY[0])
        DRIVE_Y_AXIS = JoystickAxis(Controllers.DRIVER, controllerDRIVER.L_JOY[1])
        DRIVE_ROTATION_AXIS = JoystickAxis(Controllers.DRIVER, controllerDRIVER.R_JOY[0])
        
        DRIVE_ALIGN_NOTE = commands2.button.JoystickButton(Controllers.DRIVER_CONTROLLER, controllerDRIVER.A)
        DRIVE_ALIGN_SPEAKER = commands2.button.JoystickButton(Controllers.DRIVER_CONTROLLER, controllerDRIVER.Y)
        DRIVE_ALIGN_HUMAN = commands2.button.JoystickButton(Controllers.DRIVER_CONTROLLER, controllerDRIVER.B)
        DRIVE_ALIGN_AMP = commands2.button.JoystickButton(Controllers.DRIVER_CONTROLLER, controllerDRIVER.X)
        DRIVE_ALIGN_TRAP = commands2.button.JoystickButton(Controllers.DRIVER_CONTROLLER, controllerDRIVER.START)
