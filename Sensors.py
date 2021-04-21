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
from config import pin_MUTE, pin_BATT_OFF, pin_ADC1_OUT,pin_ADC2_OUT,pin_ALARM_PWM,pin_LED1,pin_LED2,pin_LED3,pin_LED4
spkr_freq,ADC_end_voltage,ADC_start_voltage,ADC_step, 

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
    self.pi1.set_mode(pin_MUTE, pigpio.INPUT)
    self.pi1.set_mode(pin_ADC1_OUT, pigpio.INPUT)
    self.pi1.set_mode(pin_ADC2_OUT, pigpio.INPUT)
    self.pi1.set_mode(pin_BATT_OFF, pigpio.INPUT) # if a 1 is receives, using main power; if 0, using battery power
    
    
    # Initialize speaker PWM
    #TODO change pins
    self.pi1.set_PWM_dutycycle(pin_ALARM_PWM,128)
    self.pi1.set_PWM_frequency(pin_ALARM_PWM,0)
  
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

      for i in range(ADC_start_voltage, ADC_end_voltage, ADC_step):
          
          self.pi1.hardware_PWM(18, 100000, i) # Loop through PWM 
          time.sleep(0.03) # Wait to settle

          temp_comparator = self.pi1.read(pin_ADC1_OUT) 
          setpoint_comparator = self.pi1.read(pin_ADC2_OUT)
          
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

      self.read_digital_ambient_sensors()

      if (len(temp_reading_dict.values()) == 0):
        return -1

      return sum(temp_reading_dict.values()) / len(temp_reading_dict.values())
      
  '''
  Description: Is ambient sensor average in range? THIS CODE IS UNUSED
  '''    
  def ambient_temp_alarm(self):
    ambient_sensor_temp = self.get_average_temperature()
    if(ambient_sensor_temp < amb_temp_thres_min or ambient_sensor_temp > amb_temp_thres_max):
        return True
    else: 
        return False

'''
Summarizes and reads all sensors
'''
class MachineStatus():

  pi1 = pigpio.pi()
  snooze_on = False
  snooze_timer = time.perf_counter()
  
  patient = None
  ambient = None
 
  skin_temp_reading = -1
  analog_alarm_on = False

  set_point_reading = -1
  
  ambient_temp_avg = -1
  ambient_alarm_on = False

  textToDisplay = ""

  def __init__(self):
    self.patient = Patient_Sensors()
    self.ambient = Ambient_Sensors()
    self.pi1.set_mode(pin_MUTE, pigpio.INPUT)


  def update_warning(self):

    ambient_alarm_on = ambient_sensor_temp < amb_temp_thres_min or ambient_sensor_temp > amb_temp_thres_max

        # Is snooze button pressed? If so mute alarm and start timer
    if self.pi1.read(pin_MUTE) and self.analog_alarm_on and not snooze_on:
        self.snooze_on = True
        self.analog_alarm_on = False
        self.pi1.set_PWM_frequency(pin_ALARM_PWM,0) # Mute the alarm
        self.snooze_timer = time.perf_counter()
    
    if self.skin_temp_reading > skin_temp_thres_min or self.skin_temp_reading < skin_temp_thres_max: # TODO: Config the temp ranges
        # IF the alarm is not already on AND (IF the snooze button has been pressed and we are out of time, OR if the snooze is off), THEN turn alarm on if out of temp range
        if(((self.snooze_on and time.perf_counter() - self.snooze_timer >= snooze_length) or not self.snooze_on) and not analog_alarm_on):
            self.snooze_on = False
            self.analog_alarm_on = True
            self.pi1.set_PWM_frequency(pin_ALARM_PWM,spkr_freq)  # turn alarm on
    else:
        self.analog_alarm_on = False
        self.pi1.set_PWM_frequency(pin_ALARM_PWM,0) # mute    


  def update(self):
    # read each sensor and update global variables
    analog_setpoint = self.patient.read_analog_temp_and_setpoint()
    self.skin_temp_reading = analog_setpoint[0]
    self.set_point_reading = analog_setpoint[1]

    # read ambient sensor
    self.ambient_temp_avg = self.ambient.get_average_temperature()

    self.update_warning()


  def check_alarms(self):
    if (self.analog_alarm_on) :
        self.textToDisplay = "Check baby temp"
    elif (self.ambient_alarm_on):
        self.textToDisplay = "Check incubator temp"    
    else:
        self.textToDisplay = "All clear!"
    
    # falses are fill-in values for now     
    warnings = [self.analog_alarm_on or self.ambient_alarm_on, 0, 0, 0, 0]
    colors = [ self.get_color(w) for w in warnings]
    return colors

  def get_color(self, alarm):
    if alarm:
      return 'red'
    else:
      return 'dark slate grey'
