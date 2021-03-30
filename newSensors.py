import random
import pytz
import time
import pigpio

class Patient():
  pi1 = pigpio.pi()
  setpointtemp = random.randint(29,39)
  tempreading = random.randint(29,39)
  alarmOn = False
  tempSensor   = None

  def __init__(self):
    tempSensor = 0
    self.pi1.set_mode(23, pigpio.OUTPUT)
    self.pi1.write(23,False)
    self.pi1.set_PWM_dutycycle(24,200)
    self.pi1.set_PWM_frequency(24,5000)
  def setpoint(self):
      return self.setpointtemp
      
  def temperature(self):
      self.setpointtemp = random.randint(24,45)
      self.tempreading = random.randint(24,45)
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
    print(str(temp) + str(self.alarmOn))
        

    if temp > 39 or temp < 29:
        self.alarmOn = True
        self.pi1.write(23,self.alarmOn)
        return True
    else:
    
        self.alarmOn = False
        self.pi1.write(23,self.alarmOn)
        return False
    
class MachineStatus():
  patient = None
  ambient = None
  Apnea   = None
  textToDisplay = ""

  def __init__(self, pSensors, aSensors):
    self.patient = pSensors
    #self.ambient = aSensors
    #self.Apnea   = ApneaPad()

  def AC_power_state(self):
    connected = True
    if connected:
      return ''
    else:
      return ''
    
    

  def alarm_state(self):
    alarms = True # Button to mute alarms
    
    if alarms:
      a = ''
    else:
      a = ''
    return '{}'.format(a)
    
  def check_alarms(self):
      
    temp_warning = self.patient.temp_warning()
                 
    '''
    rh_warning = (self.ambient.rh < 40) | (self.ambient.rh > 77)
    apnea_warning = self.Apnea.check_apnea()
    textToDisplay = "Apnea level warning"
    hr_warning = (self.patient.hr < 120) | (self.patient.hr > 160)
    o2_warning = (self.patient.o2 < 95) | (self.patient.o2 > 100)

    warnings = [
                  temp_warning,   # T
                  rh_warning,     # RH
                  apnea_warning,  # A
                  hr_warning,     # HR
                  o2_warning      # O2
                  
               ]
    if (temp_warning) :
        self.textToDisplay = "Check tempearture"
    elif (hr_warning):
        self.textToDisplay = "Check heart rate"
    elif (o2_warning):
        self.textToDisplay = "Check oxygen saturation"
    elif(apnea_warning):
        self.textToDisplay = "Check apnea levels"
    
        
    
    '''
         
    warnings = [ temp_warning]
    colors = [ self.get_color(w) for w in warnings]
    return colors

  def get_color(self, alarm):
    if alarm:
        
      return 'red'
    else:
      return 'dark slate grey'
