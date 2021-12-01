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
from gpiozero.pins.mock import MockFactory, MockPWMPin
from config import *
import glob
import time

Device.pin_factory = MockFactory(pin_class=MockPWMPin)

class PeripheralBus:

  def __init__(self, stateFile):

    self.machineState = stateFile

    self.setPointIDevice = DigitalInputDevice(PIN_ADC1_CMPR)
    self.ctrlTempIDevice = DigitalInputDevice(PIN_ADC2_CMPR)

    self.batteryIDevice = DigitalInputDevice(PIN_BATT_OFF)

    self.heaterIDevice1 = DigitalInputDevice(12)
    self.heaterIDevice2 = DigitalInputDevice(16)
    self.heaterIDevice3 = DigitalInputDevice(20)
    self.heaterIDevice4 = DigitalInputDevice(21)

    # need to make own wrapped object
    self.alarmODevice = DigitalOutputDevice(10)
    self.adcPwmODevice = PWMOutputDevice(18)

    self.snoozeButton = gpiozero.Button(11)
    self.snoozeButton.when_pressed = self.snoozeHandler

    self.preheatButton = gpiozero.Button(9)
    self.preheatButton.when_pressed = self.preheatHandler
    
  def preheatHandler(self):
    self.machineState.is_preheat = True
    print("HERE!")

  def snoozeHandler(self):
    self.machineState.is_snoozed = True
    
  def read_digital_temp_raw(self, device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

  def read_digital_sensors(self):
    if PC_DEV:
      return {"A" : 36, "B" : 36, "C" : 36, "D" : 36}

    file_suffix = '/w1_slave'
    base_dir = '/sys/bus/w1/devices/'
    device_folders = glob.glob(base_dir + '28*')

    result_dict = dict()

    for d_f in device_folders:
        device_file = d_f + file_suffix
        lines = self.read_digital_temp_raw(device_file)
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_digital_temp_raw(device_file)
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            result_dict[d_f] = temp_c

    return result_dict 

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
    for i in range(ADC_START_VOLTAGE, ADC_START_VOLTAGE, ADC_STEP):
        
        self.adcPwmODevice.value = i
        time.sleep(0.03) # Wait to settle

        temp_comparator = self.ctrlTempIDevice
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

  def update(self):
    
    ## Grab readings from peripherals
    # Digital Temperature Sensors (Ambient + Probe)
    digital_temp_reading = self.read_digital_sensors()
    self.machineState.ambientSensorReadings = digital_temp_reading.values()
    self.machineState.probeReading = digital_temp_reading['A']

    # Battery Signal
    self.machineState.batteryStaus = self.batteryIDevice.value

    # Heater Statuses
    self.machineState.heaterHealth = self.read_heater_health

    # ADC Readings
    adc_dict = self.read_ADC_sensors()
    self.machineState.setPointReading = adc_dict["Setpoint"]
    self.machineState.analogTempReading = adc_dict["Temperature"]



    




