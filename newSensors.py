import random
import pytz
import time
import pigpio
from w1thermsensor import W1ThermSensor, Sensor
snoozebut = 16

class Patient():
  pi1 = pigpio.pi()
  setpointtemp = 32.0
  tempreading = 0.0
  alarmOn = False
  timer = time.perf_counter()
  tempSensor   = None
  snooze   = False

  def __init__(self):
    tempSensor = 0
    # snooze button is pin 16
    self.pi1.set_mode(snoozebut, pigpio.INPUT)
    self.pi1.set_mode(6, pigpio.INPUT)
    self.pi1.set_mode(26, pigpio.INPUT)
    
    
    # speaker PWM
    self.pi1.set_PWM_dutycycle(24,128)
    self.pi1.set_PWM_frequency(24,0000)
  def setpoint(self):
      return self.setpointtemp
      
  def temperature(self):
      
      val1 = False
      val2 = True
      x = 0
      y = 0
      for i in range(200000, 1000000, 1000):
          self.pi1.hardware_PWM(18, 100000, i)
          time.sleep(0.03)
          x = self.pi1.read(6)
          y = self.pi1.read(26)
          #print(i)
          if(x == 1 and val1 == False):
              self.tempreading = ((3.3 * float(i) / 1000000) - 0.5) * 100
              print(self.tempreading)
              val1 = True
          #if(y == 1):
          #    self.setpointemp = y
          #    val2 = True
          if(val2 and val1):
              break
        
              
      self.setpointtemp = 35.0
      #self.tempreading = 32.0
      

      return self.tempreading

  def temp_warning(self):
    if self.pi1.read(snoozebut):
        snooze = True
        self.alarmOn = False
        self.pi1.set_PWM_frequency(24,0000)
        self.timer = time.perf_counter()
        
    temp = self.tempreading
    
    print(str(temp) + str(self.alarmOn))
        

    if temp > 39 or temp < 20:
        if((self.snooze and time.perf_counter() - self.timer >= 120 ) or not self.snooze):
            self.snooze = False
            self.alarmOn = True
            self.pi1.set_PWM_frequency(24,5000)
            return True
    else:
        self.alarmOn = False
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

  def temperature(self):
      '''
      i = 0
      for sensor in W1ThermSensor.get_available_sensors([Sensor.DS18B20]):
          self.tempSensor += sensor.get_temperature()
          i = i + 1
          
      if(not(i == 0) ):
          self.tempSensor = (float)(self.tempSensor)/i
      
      return self.tempSensor
      '''
      return random.randint(30,40)
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

  def AC_power_state(self):
    connected = True
    # can use \U000023FB and switch color to determine if disconencted or not
    if connected:
      return ' '
    else:
      return ''
    
    
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
