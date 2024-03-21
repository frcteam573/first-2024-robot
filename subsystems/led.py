import math

import commands2
import wpilib
import wpilib.drive
import rev

class LED(commands2.SubsystemBase):
  
  def __init__(self) -> None:
    super().__init__()
    
    self.blinkin = wpilib.Spark(0) # Change later
    
  # // COLOR FUNCTION LIST \\ #
  
  '''Value list: https://www.revrobotics.com/content/docs/REV-11-1105-UM.pdf'''
  
  def setBlackLed(self): # Off
    self.blinkin.set(0.99)
    #print('Black')
  
  def setRedLed(self): 
    self.blinkin.set(0.61)
   # print('Red')
  
  def setYellowLed(self):
    self.blinkin.set(0.69)
    #print('Yellow')
  
  def setOrangeLed(self):
    self.blinkin.set(0.65)
   # print('Orange')
   
  def setGreenLed(self):
    self.blinkin.set(0.77)
    #print('Green')