'''
Author: Hussain Miyaziwala
Last Updated: 12/6/21
Description:
  Contains logic for reading all sensors and generating warnings.
'''

import random
from gpiozero.output_devices import DigitalOutputDevice, PWMOutputDevice
import pytz
import time
import gpiozero
from gpiozero import DigitalInputDevice
from gpiozero import Device
from gpiozero.pins.pigpio import PiGPIOFactory
from config import *
import glob
import time

class PeripheralBus:

  def __init__(self, stateFile):
    factory = PiGPIOFactory()

    self.machineState = stateFile

    self.alarmDevice = AlarmDevice(stateFile)

    self.probeAddress = -1
    self.probePowerDevice = DigitalOutputDevice(PIN_PROBE_POWER, initial_value=True)

    self.heaterCtrlReqIDevice = DigitalInputDevice(PIN_THERM_IN)
    self.heaterCommandIDevice = DigitalInputDevice(PIN_THERM_OUT)
    
    self.setPointIDevice = DigitalInputDevice(PIN_SET_POINT_CMPR)
    self.ctrlTempIDevice = DigitalInputDevice(PIN_CTRL_SNSR_CMPR)

    self.heaterIDevice1 = DigitalInputDevice(PIN_HEATER_CHECK_1)
    self.heaterIDevice2 = DigitalInputDevice(PIN_HEATER_CHECK_2)
    self.heaterIDevice3 = DigitalInputDevice(PIN_HEATER_CHECK_3, pin_factory=factory)
    self.heaterIDevice4 = DigitalInputDevice(PIN_HEATER_CHECK_4, pin_factory=factory)

    self.adcPwmODevice = PWMOutputDevice(PIN_ADC_PWM, pin_factory=factory)
    self.alarmLedODevice = DigitalOutputDevice(PIN_ALARM_LED)
    self.preheatLedODevice = DigitalOutputDevice(PIN_PREHEAT_LED)

    self.snoozeButton = gpiozero.Button(PIN_SNOOZE_BTN)
    self.snoozeButton.when_pressed = self.snoozeHandler

    self.preheatButton = gpiozero.Button(PIN_PREHEAT_BTN)
    self.preheatButton.when_pressed = self.preheatHandler
    
  def preheatHandler(self):
    self.machineState.is_preheating = not self.machineState.is_preheating

  def snoozeHandler(self):
    self.machineState.is_snooze_requested = True

  # Read raw file and return lines as list  
  def read_digital_temp_raw(self, device_file):
    try:
      f = open(device_file, 'r')
      lines = f.readlines()
      f.close()
    except FileNotFoundError:
      lines = []
    return lines

  '''
  Reads digital sensors.
  Digital sensors in the Rpi are devices and thus must be read from a file
  Returns: Dictionary of sensor serial numbers to temperature value
  '''
  def read_digital_sensors(self):
    start = time.time()
    file_suffix = '/w1_slave'
    base_dir = '/sys/bus/w1/devices/'
    device_folders = glob.glob(base_dir + '28*')

    result_dict = dict()

    # Grab temperature from each device file 
    for d_f in device_folders:
        device_file = d_f + file_suffix
        serial_id = d_f.split('/')[-1]
        lines = self.read_digital_temp_raw(device_file)
        attempt_counter = 0
        try:
            while lines[0].strip()[-3:] != 'YES': # assert that CRC code is correct
                time.sleep(0.2) # wait before trying again
                lines = self.read_digital_temp_raw(device_file)
                attempt_counter += 1
                if attempt_counter > 3: # move on after 3 tries
                  raise TimeoutError
            equals_pos = lines[1].find('t=')
        except IndexError:
          continue
        except TimeoutError:
          continue
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            # temp_f = temp_c * 9.0 / 5.0 + 32.0
            result_dict[serial_id] = temp_c

    # remove any errored values (shows up as zero... hopefully baby is not freezing)
    result_filtered = {key:value for (key, value) in result_dict.items() if value != 0 }
    self.machineState.alarmCodes["Digital Sensor Disconnect"] = False

    # check error for no sensors 
    if len(result_filtered.values()) == 0:
      self.machineState.alarmCodes["Digital Sensor Disconnect"] = True
  
    return result_filtered 

  def read_heater_health(self):
    health_dict = dict()
    health_dict[1] = self.heaterIDevice1.value
    health_dict[2] = self.heaterIDevice2.value
    health_dict[3] = self.heaterIDevice3.value
    health_dict[4] = self.heaterIDevice4.value
    return health_dict

  '''
  Read the ADC devices: The setpoint potentiometer and the TMP36
  Uses PWM ouptut to create a range of voltages that is compared to the sensor via an OpAmp
  This algorithm uses binary search to find the voltage in {ADC_SEARCH_CYLCES} cycles
  Returns: Dictionary for the temperature and set point readings
  '''
  def read_ADC_sensors_binary(self):
    low = ADC_START_VOLTAGE
    high = ADC_END_VOLTAGE
    lower_limit = ADC_VOLTAGE_LOWER
    upper_limit = ADC_VOLTAGE_UPPER

    # Find Set Point
    setpoint_tmp = 0
    count = 0
    x = (high + low) / 2
    while (count < ADC_SEARCH_CYCLES):
      count += 1
      self.adcPwmODevice.value = x
      time.sleep(0.03) # Wait to settle
      setpoint_comparator = self.setPointIDevice.value
      if (setpoint_comparator == 1):
        x -= ((high - low) / (pow(2,(count+1))))
      else:
        x += ((high - low) / (pow(2,(count+1))))
      
    if x > upper_limit or x < lower_limit:
      # Set Point not found
      print("Unable to read setpoint")
    else:
      setpoint_tmp = (x * 3.3 * 1000 - 500 ) / 10

    # Find Controller Temp
    control_sensor_tmp = 0
    count = 0
    x = (high + low) / 2
    while (count < 20):
      count += 1
      self.adcPwmODevice.value = x
      time.sleep(0.03) # Wait to settle
      tmp_comparator = self.ctrlTempIDevice.value
      if (tmp_comparator == 1):
        x -= ((high - low) / (pow(2,(count+1))))
      else:
        x += ((high - low) / (pow(2,(count+1))))
      
    if x > upper_limit or x < lower_limit:
      # Controller Temp not found
      print("Unable to read controller temp")
      self.machineState.alarmCodes["Control Sensor Malfunction"] = True
    else:
      self.machineState.alarmCodes["Control Sensor Malfunction"] = False
      control_sensor_tmp = (x * 3.3 * 1000 - 500 ) / 10

    return {"Temperature" : control_sensor_tmp, "Setpoint" : setpoint_tmp}

  def writeOutput(self):
    self.alarmDevice.update()
    
    if self.machineState.soundAlarm:
      self.alarmLedODevice.on()
    else:
      self.alarmLedODevice.off()

    if self.machineState.is_preheating:
      self.preheatLedODevice.on()
    else:
      self.preheatLedODevice.off()


  def findProbe(self):

    # get list of current devices
    file_suffix = '/w1_slave'
    base_dir = '/sys/bus/w1/devices/'
    
    device_folders_before = glob.glob(base_dir + '28*')

    if len(device_folders_before) == 0:
      return -1

    # turn off power to probe
    self.probePowerDevice.off()
    time.sleep(0.1)

    # get list of devices now
    device_folders_after = glob.glob(base_dir + '28*')
    diff = list(set(device_folders_before) - set(device_folders_after))

    if (diff != 1):
      print("PROBE FINDING ERROR")
      return -1

    # return the difference
    return diff[0].split('/')[-1]

  def update(self):
    t = time.time()
    ## Grab readings from peripherals
    # Digital Temperature Sensors (Ambient + Probe)
    # Logic to determine if probe needs to be updated 
    prev_num_digital_sensors = len(self.machineState.ambientSensorReadings)
    digital_temp_reading = self.read_digital_sensors()

    if (prev_num_digital_sensors != self.machineState.ambientSensorReadings):
      # determine the probe's address
      self.probeAddress = self.findProbe()

    # Grab probe reading from dict
    self.machineState.probeReading = digital_temp_reading.get(self.probeAddress, -1)

    # Grab all digital readings (includes probe for now...)
    self.machineState.ambientSensorReadings = digital_temp_reading.values()

    # Remove the probe reading from the digital sensor set
    if self.machineState.probeReading in self.machineState.ambientSensorReadings: 
      self.machineState.ambientSensorReadings.remove(self.machineState.ambientSensorReadings)
   

    print("Digital read time:", time.time() - t)
    t = time.time()

    # Heater Statuses
    self.machineState.heaterHealth = self.read_heater_health()
    print("Heater read time:", time.time() - t)
    t = time.time()

    # ADC Readings
    adc_dict = self.read_ADC_sensors_binary()
    self.machineState.setPointReading = adc_dict["Setpoint"]
    self.machineState.analogTempReading = adc_dict["Temperature"]
    print("ADC read time:", time.time() - t)

    # Temperature Fuse + Heater States
    self.machineState.physicalControlLine = self.heaterCtrlReqIDevice.value
    self.machineState.physicalHeaterCommand = self.heaterCommandIDevice.value

class AlarmDevice:

  def __init__(self, stateFile):
    self.machineState = stateFile
    self.alarmODevice = PWMOutputDevice(PIN_ALARM_PWM, frequency=2000)
    self.alarmODevice.off()
    self.startTime = 0
    self.twoToneTime = 0
    self.twoToneFlip = False

  def update(self):

    if (self.machineState.soundAlarm):
       curr = time.time()
       if (curr - self.twoToneTime > 1):
         self.twoToneFlip = not self.twoToneFlip
         self.twoToneTime = curr


    if self.machineState.is_snooze_requested:
      self.machineState.is_snooze_requested = False
      self.machineState.is_snoozed = True
      self.startTime = time.time()

    # see if snooze over
    # TODO: Change to update state file
    if (self.machineState.is_snoozed and time.time() - self.startTime > SNOOZE_LENGTH):
      self.machineState.is_snoozed = False
    else:
      self.machineState.snooze_countdown = round(SNOOZE_LENGTH - (time.time() - self.startTime))

    # sound alarm
    if (self.machineState.soundAlarm and
       not self.machineState.is_snoozed and
       not self.machineState.is_preheating):

       if (self.twoToneFlip):
        self.alarmODevice.frequency(2000)
       else:
        self.alarmODevice.frequency(4000)

       self.alarmODevice.on()
    else:
      self.alarmODevice.off()

    




