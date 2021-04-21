'''
Author:
Last Updated:
Description:
  Contains logic for reading all sensors and generating warnings.
'''

import random
import pytz
import time
import pigpio
from w1thermsensor import W1ThermSensor, Sensor

# TODO: Move to configuration and rename (pin_name)
snoozebut = 21
power = 15 # if a 1 is receives, using main power; if 0, using battery power

class Patient():
  pi1 = pigpio.pi()
  set_point_temp = 0.0
  skin_temp_reading = 0.0

  alarm_on = False
  snooze_timer = time.perf_counter()
  is_snooze   = False

'''
Initialize pin modes
'''
  def __init__(self):
    # TODO: Change hardcoded pins to config references
    # is_snooze button is pin 16
    self.pi1.set_mode(snoozebut, pigpio.INPUT)
    self.pi1.set_mode(6, pigpio.INPUT)
    self.pi1.set_mode(26, pigpio.INPUT)
    self.pi1.set_mode(power, pigpio.INPUT)
    
    
    # Initialize speaker PWM
    #TODO change pins
    self.pi1.set_PWM_dutycycle(24,128)
    self.pi1.set_PWM_frequency(24,0)
  
  # TODO: Change to get_setpoint (used in patient)
  def setpoint(self):
      return self.set_point_temp
      
  def read_analog_temp_and_setpoint(self):
      
      temp_found = False
      setpoint_found = False
      temp_comparator = 0
      setpoint_comparator = 0
      for i in range(200000, 1000000, 1000): # TODO Config: starting, ending, interation
          
          self.pi1.hardware_PWM(18, 100000, i) # Loop through PWM 
          time.sleep(0.03) # Wait to settle

          temp_comparator = self.pi1.read(6) #TODO Pin numbers
          setpoint_comparator = self.pi1.read(26)
          
          if(temp_comparator == 1 and temp_found == False):
              self.skin_temp_reading = ((3.3 * float(i) / 1000000) - 0.5) * 100
             # print("SkinTemp:",self.skin_temp_reading)
              temp_found = True

          if(setpoint_comparator == 1 and setpoint_found == False):
              self.set_point_temp = ((3.3 * float(i) / 1000000) - 0.5) * 100
             # print("Set_Point_Temp:",self.set_point_temp)
              setpoint_found = True
              
          if(setpoint_found and temp_found):
              break
        
              
      #self.set_point_temp = 35.0
      #self.skin_temp_reading = 32.0
      

      return self.skin_temp_reading

  def temp_warning(self):
    if self.pi1.read(snoozebut):
        is_snooze = True
        self.alarm_on = False
        self.pi1.set_PWM_frequency(24,0000)
        self.snooze_timer = time.perf_counter()
        
    temp = self.skin_temp_reading
    
    print(str(temp) + str(self.alarm_on))
        

    if temp > 39 or temp < 20:
        if((self.is_snooze and time.perf_counter() - self.snooze_timer >= 120 ) or not self.is_snooze):
            self.is_snooze = False
            self.alarm_on = True
            self.pi1.set_PWM_frequency(24,5000)
            return True
    else:
        self.alarm_on = False
        self.pi1.set_PWM_frequency(24,0000)
        return False
    
''' The "Environment" class refers to the sensor
    readings inside the incubator. Only 'tempSensor' is incorporated.
    More cn be added such as the humidity sensor. 
'''
class Environment():
  tempSensor = 0 # can change this to NONE if you want tempSensor to point to an object vs a value
  rhSensor   = None
  rh         = 0

  def __init__(self):
    #self.tempSensor = OneWire.TempSensor()
    #self.rhSensor   = DHT22(board.D16)
    self.tempSensor = 35

  def read_analog_temp_and_setpoint(self):
      
      i = 0
      self.tempSensor = 0
      for sensor in W1ThermSensor.get_available_sensors([Sensor.DS18B20]):
          self.tempSensor += sensor.get_temperature()
          print("AmbientTemp:",sensor.get_temperature())
          i = i + 1
          
      if(not(i == 0) ):
          self.tempSensor = (float)(self.tempSensor)/i
      
      return self.tempSensor
      
  def temp_warning(self):
    if(self.tempSensor < 30.5 or self.tempSensor > 40.5):
        return True
    else: 
        return False  # depends on set point. To be added later

 

class MachineStatus():
  patient = None
  ambient = None
  Apnea   = None
  textToDisplay = ""

  def __init__(self, pSensors, aSensors):
    self.patient = pSensors
    self.ambient = aSensors
    #self.Apnea   = ApneaPad()

    
    
  '''
  def alarm_state(self):
    alarms = True # Button to mute alarms
    
    if alarms:
      a = ''
    else:
      a = ''
    return '{}'.format(a)
  ''' 
  def check_alarms(self):
      
    temp_warning = self.patient.temp_warning() | self.ambient.temp_warning()
    print("self_patient" + str(self.patient.temp_warning() ))
    print("self_ambient" + str(self.ambient.temp_warning() ))
                 
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
    '''           
    if (self.patient.temp_warning()) :
        self.textToDisplay = "Check baby temp"
    elif (self.ambient.temp_warning()):
        self.textToDisplay = "Check incubator temp"    
    else:
        self.textToDisplay = "All clear!"
    '''
    elif (hr_warning):
        self.textToDisplay = "Check heart rate"
    elif (o2_warning):
        self.textToDisplay = "Check oxygen sat"
    elif(apnea_warning):
        self.textToDisplay = "Check apnea levels"
    '''

        
        
    
        
    
    
    # falses are fill-in values for now     
    warnings = [ temp_warning, 0, 0, 0, 0]
    colors = [ self.get_color(w) for w in warnings]
    return colors

  def get_color(self, alarm):
    if alarm:
        
      return 'red'
    else:
      return 'dark slate grey'
