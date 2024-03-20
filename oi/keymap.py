import commands2.button
import wpilib
from robotpy_toolkit_7407.oi import (
    JoystickAxis,
    XBoxController,
)

controllerDRIVER = XBoxController
controllerOPERATOR = XBoxController

class Controllers:
    DRIVER = 0
    OPERATOR = 1

    DRIVER_CONTROLLER = wpilib.Joystick(0)
    OPERATOR_CONTROLLER = wpilib.Joystick(1)

class Keymap:
    class Intake:
        INTAKE_IN = commands2.button.JoystickButton(Controllers.OPERATOR_CONTROLLER, controllerOPERATOR.LB)
        INTAKE_OUT = commands2.button.JoystickButton(Controllers.OPERATOR_CONTROLLER, controllerOPERATOR.RB)
        SHOOTER = JoystickAxis(Controllers.OPERATOR, controllerOPERATOR.LT)
        TRAP_HOOD = commands2.button.JoystickButton(Controllers.OPERATOR_CONTROLLER, controllerOPERATOR.SELECT)
        TRANSFER = JoystickAxis(Controllers.OPERATOR, controllerOPERATOR.RT)
        
        FLOOR_POSITION = commands2.button.JoystickButton(Controllers.OPERATOR_CONTROLLER, controllerDRIVER.A)
        SPEAKER_POSITION = commands2.button.JoystickButton(Controllers.OPERATOR_CONTROLLER, controllerDRIVER.Y)
        HUMAN_POSITION = commands2.button.JoystickButton(Controllers.OPERATOR_CONTROLLER, controllerDRIVER.B)
        AMP_POSITION = commands2.button.JoystickButton(Controllers.OPERATOR_CONTROLLER, controllerDRIVER.X)
        TRAP_POSITION = commands2.button.JoystickButton(Controllers.OPERATOR_CONTROLLER, controllerDRIVER.START)
        
    class Shoulder:
        SHOULDER_AXIS = JoystickAxis(Controllers.OPERATOR, controllerOPERATOR.L_JOY[1])
        SHOULDER_TRIM_UP = commands2.button.POVButton(Controllers.OPERATOR_CONTROLLER, 0)
        SHOULDER_TRIM_DOWN = commands2.button.POVButton(Controllers.OPERATOR_CONTROLLER, 180)
        
    class Climber:
        CLIMBER_UP = commands2.button.JoystickButton(Controllers.DRIVER_CONTROLLER, controllerDRIVER.RB)
        CLIMBER_DOWN = commands2.button.JoystickButton(Controllers.DRIVER_CONTROLLER, controllerDRIVER.LB)
    
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
