'''
Author:
Last Updated:
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
#from gpiozero.pins.mock import MockFactory, MockPWMPin
from config import *
import glob
import time

#if PC_DEV:
 # Device.pin_factory = MockFactory(pin_class=MockPWMPin)

class PeripheralBus:

  def __init__(self, stateFile):

    factory = PiGPIOFactory()

    self.machineState = stateFile

    self.alarmDevice = AlarmDevice(stateFile)

    self.heaterCtrlReqIDevice = DigitalInputDevice(PIN_THERM_IN)
    self.heaterCommandIDevice = DigitalInputDevice(PIN_THERM_OUT)
    
    self.setPointIDevice = DigitalInputDevice(PIN_SET_POINT_CMPR)
    self.ctrlTempIDevice = DigitalInputDevice(PIN_CTRL_SNSR_CMPR)

    self.heaterIDevice1 = DigitalInputDevice(PIN_HEATER_CHECK_1)
    self.heaterIDevice2 = DigitalInputDevice(PIN_HEATER_CHECK_2)
    self.heaterIDevice3 = DigitalInputDevice(PIN_HEATER_CHECK_3, pin_factory=factory)
    self.heaterIDevice4 = DigitalInputDevice(PIN_HEATER_CHECK_4, pin_factory=factory)

    self.adcPwmODevice = PWMOutputDevice(PIN_ADC_PWM, pin_factory=factory)
    self.adcPwmODevice.value = 1
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
    
  def read_digital_temp_raw(self, device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

  def read_digital_sensors(self):
    file_suffix = '/w1_slave'
    base_dir = '/sys/bus/w1/devices/'
    device_folders = glob.glob(base_dir + '28*')

    result_dict = dict()

    for d_f in device_folders:
        device_file = d_f + file_suffix
        serial_id = d_f.split('/')[-1]
        lines = self.read_digital_temp_raw(device_file)
        attempt_counter = 0
        try:
            while lines[0].strip()[-3:] != 'YES':
                time.sleep(0.2)
                lines = self.read_digital_temp_raw(device_file)
                attempt_counter += 1
                if attempt_counter > 10:
                  raise TimeoutError
            equals_pos = lines[1].find('t=')
        except IndexError:
          continue
        except TimeoutError:
          continue
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            result_dict[serial_id] = temp_c

    result_filtered = {key:value for (key, value) in result_dict.items() if value != 0 }

    if len(result_dict.values()) == 0:
      print("Nothing found")
      self.machineState.alarmCodes["Digital Sensor Disconnect"] = True
      return {'0' : 0}
      
    self.machineState.alarmCodes["Digital Sensor Disconnect"] = False
    return result_filtered 

  def read_heater_health(self):
    if PC_DEV:
      return [1,1,1,1]

    health_dict = dict()
    health_dict[1] = self.heaterIDevice1.value
    health_dict[2] = self.heaterIDevice2.value
    health_dict[3] = self.heaterIDevice3.value
    health_dict[4] = self.heaterIDevice4.value
    return health_dict

  def read_ADC_sensors(self):
    if PC_DEV:
      return {"Temperature" : 36, "Setpoint" : 37}

    temp_found = False
    setpoint_found = False
    temp_comparator = 0
    setpoint_comparator = 0

    temp_reading = 0  
    set_point_temp = 0 

    # TODO: ADC Start and End Voltages need to translate to value between 0 and 1
    for v in range(int(ADC_START_VOLTAGE), int(ADC_START_VOLTAGE), int(ADC_STEP)):
        
        i = float(v) / ADC_MAG_ADJ

        self.adcPwmODevice.value = i
        time.sleep(0.03) # Wait to settle

        temp_comparator = self.ctrlTempIDevice.value
        setpoint_comparator = self.setPointIDevice.value
        
        # Read for analog temp sensor
        if(temp_comparator == 1 and temp_found == False):
            temp_reading = ((3.3 * float(i) / 1000000) - 0.5) * 100
            temp_found = True

        # Read for set point
        if(setpoint_comparator == 1 and setpoint_found == False):
            set_point_temp = ((3.3 * float(i) / 1000000) - 0.5) * 100
            setpoint_found = True
            
        if(setpoint_found and temp_found):
            break

    if not(temp_found):
      print("Unable to read skin sensor")
    if not (setpoint_found):
      print("Unable to read ambient temperature")
        
    return {"Temperature" : temp_reading, "Setpoint" : set_point_temp}

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

  def update(self):
    ## Grab readings from peripherals
    # Digital Temperature Sensors (Ambient + Probe)
    digital_temp_reading = self.read_digital_sensors()
    self.machineState.ambientSensorReadings = digital_temp_reading.values()
    self.machineState.probeReading = list(digital_temp_reading.values())[0]

    # Heater Statuses
    self.machineState.heaterHealth = self.read_heater_health()

    # ADC Readings
    adc_dict = self.read_ADC_sensors()
    self.machineState.setPointReading = adc_dict["Setpoint"]
    self.machineState.analogTempReading = adc_dict["Temperature"]

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
         self.twoToneFlip = not self.twoToneFilp
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
      self.machineState.snooze_countdown = round(time.time() - self.startTime)

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

    




