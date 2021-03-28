import random
import pytz
import time
class Patient():
  setpointtemp = random.randint(29,39)
  tempreading = random.randint(29,39)
  alarmOn = False
  timer = time.perf_counter()
  tempSensor   = None

  def __init__(self):
    tempSensor = 0
  def setpoint(self):
      return self.setpointtemp
      
  def temperature(self):
      # determine the set point value with PWM 
      # determine the temperatuer sensor reading through PWM
      #update the global vars


    return self.tempreading

  def temp_warning(self):
    temp = self.tempreading
    print("in alarm" + str(self.alarmOn))
    
    '''
    if the baby is too warm: orange light (red and green)
    
    if the baby is too cold : blue light
    if the baby is perfect: green light
    
    if something other than temperature is wrong: light the Red LED (NOT IMPLEMENTED YET)
    
    if tempSensor > 39 or tempSensor < 29:
        sound alarm
        alarmOn = True
        start timer
        
    else :
        do nothing
        
    
    '''

    if temp < 36.0:
      return True
    elif temp > 37.5:
      return True
    else:
      return False
