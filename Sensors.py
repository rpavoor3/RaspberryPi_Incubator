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

class Patient_Sensors():
  pi1 = pigpio.pi()
  set_point_temp = 0.0
  skin_temp_reading = 0.0

  alarm_on = False
  snooze_timer = time.perf_counter()
  snooze_on   = False

  '''
  Initialize pin modes
  '''
  def __init__(self):
    # TODO: Change hardcoded pins to config references
    # snooze_on button is pin 16
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
  
  '''
  Function to use the PWM ADC Comparator Circuit to read the analog temperature sensor and the set point potentiometer
  Returns: {analog_reading, set_point_reading} in degrees C
  '''
  def read_analog_temp_and_setpoint(self):
     
      temp_found = False
      setpoint_found = False
      temp_comparator = 0
      setpoint_comparator = 0

      self.skin_temp_reading = 0
      self.set_point_temp = 0

      for i in range(200000, 1000000, 1000): # TODO Config: starting, ending, interation
          
          self.pi1.hardware_PWM(18, 100000, i) # Loop through PWM 
          time.sleep(0.03) # Wait to settle

          temp_comparator = self.pi1.read(6) #TODO Pin numbers
          setpoint_comparator = self.pi1.read(26)
          
          # Read for analog temp sensor
          if(temp_comparator == 1 and temp_found == False):
              self.skin_temp_reading = ((3.3 * float(i) / 1000000) - 0.5) * 100
             # print("SkinTemp:",self.skin_temp_reading)
              temp_found = True

          # Read for set point
          if(setpoint_comparator == 1 and setpoint_found == False):
              self.set_point_temp = ((3.3 * float(i) / 1000000) - 0.5) * 100
             # print("Set_Point_Temp:",self.set_point_temp)
              setpoint_found = True
              
          if(setpoint_found and temp_found):
              break

      if (not(setpoint_found) or not(temp_found)):
        print("Unable to read")

      return {"Temperature" : self.skin_temp_reading, "Setpoint" : self.set_point_temp}


  def alarm_hardware_control(self):

    # Is snooze button pressed? If so mute alarm and start timer
    if self.pi1.read(snoozebut) and self.alarm_on and not snooze_on:
        snooze_on = True
        self.alarm_on = False
        self.pi1.set_PWM_frequency(24,0) # Mute the alarm TODO: pin number
        self.snooze_timer = time.perf_counter()
        
    temp = self.skin_temp_reading
    
    #print(str(temp) + str(self.alarm_on))
    if temp > 39 or temp < 20: # TODO: Config the temp ranges
        # IF the alarm is not already on AND (IF the snooze button has been pressed and we are out of time, OR if the snooze is off), THEN turn alarm on if out of temp range
        if(((self.snooze_on and time.perf_counter() - self.snooze_timer >= 120) or not self.snooze_on) and not alarm_on):
            self.snooze_on = False
            self.alarm_on = True
            self.pi1.set_PWM_frequency(24,5000)  # turn alarm on # TODO: Config
    else:
        self.alarm_on = False
        self.pi1.set_PWM_frequency(24,0) # mute    
    
    return self.alarm_on
    
''' The "Ambient_Sensors" class refers to the sensor
    readings inside the incubator. Only 'ambient_sensor_temp' is incorporated.
    More can be added such as the humidity sensor. 
'''
class Ambient_Sensors():

  temp_reading_dict = {}
  alarm_on = False

  '''
  Description: Reads temperature readings from digital sensors. Uses W1ThermSensor library.
  Returns: Dictionary of temp sensors mapped to their readings
  '''
  def read_digital_ambient_sensors(self):
      
      self.temp_reading_dict = {}

      for sensor in W1ThermSensor.get_available_sensors([Sensor.DS18B20]):
        readings[sensor.id] = sensor.get_temperature()

      return self.temp_reading_dict

      # readings.values().sum() / reading.values().len()

  '''
  Description: Averages reading dictionary for display.
  Returns: Average reading, -1 if no sensors
  '''
  def get_average_temperature():

      if (len(temp_reading_dict.values()) == 0):
        return -1

      return sum(temp_reading_dict.values()) / len(temp_reading_dict.values())
      
  '''
  Description: Is ambient sensor average in range? THIS CODE IS UNUSED
  '''    
  def ambient_temp_alarm(self):
    ambient_sensor_temp = self.get_average_temperature()
    if(ambient_sensor_temp < 30.5 or ambient_sensor_temp > 40.5):
        return True
    else: 
        return False

'''
Summarizes and reads all sensors
'''
class MachineStatus():
  
  patient = None
  ambient = None
 
  skin_temp_reading = -1
  analog_alarm_on = False

  set_point_reading = -1
  
  ambient_temp_reading = -1
  ambient_alarm_on = False

  textToDisplay = ""

  def __init__(self):
    self.patient = Patient_Sensors()
    self.ambient = Ambient_Sensors()

  def update_state(self):
    # read each sensor and update global variables
    analog_setpoint = self.patient.read_analog_temp_and_setpoint()
    self.skin_temp_reading = analog_setpoint[0]
    self.set_point_reading = analog_setpoint[1]

    # read ambient sensor
    ambient_temp_reading = self.ambeint.
  def check_alarms(self):
                  
    if (self.patient.alarm_hardware_control()) :
        self.textToDisplay = "Check baby temp"
    elif (self.ambient.alarm_hardware_control()):
        self.textToDisplay = "Check incubator temp"    
    else:
        self.textToDisplay = "All clear!"
    
    # falses are fill-in values for now     
    warnings = [ alarm_hardware_control, 0, 0, 0, 0]
    colors = [ self.get_color(w) for w in warnings]
    return colors

  def get_color(self, alarm):
    if alarm:
        
      return 'red'
    else:
      return 'dark slate grey'
