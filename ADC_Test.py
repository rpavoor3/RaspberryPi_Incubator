from tkinter import *
from config import *
from signal import pause
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



def read_ADC_sensors_binary():
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
      adcPwmODevice.value = x / DIGITAL_VOLTAGE
      print(x)
      time.sleep(0.4) # Wait to settle
      setpoint_comparator = ctrlTempIDevice.value
      if (setpoint_comparator == 0):
        print("TOO HIGH\n")
        x -= ((high - low) / (pow(2,(count+1))))
      else:
        print("TOO LOW\n")
        x += ((high - low) / (pow(2,(count+1))))
      
    if x > upper_limit or x < lower_limit:
      # Set Point not found
      
      print("Unable to read setpoint", x)
    else:
      setpoint_tmp = x #(x * 3.3 * 1000 - 500 ) / 10


    return {"Setpoint" : setpoint_tmp}

def comparator_test():
    adcPwmODevice.value = 0.079
    print(ctrlTempIDevice.value)

low = ADC_START_VOLTAGE
high = ADC_END_VOLTAGE
lower_limit = ADC_VOLTAGE_LOWER
upper_limit = ADC_VOLTAGE_UPPER

factory = PiGPIOFactory()

adcPwmODevice = PWMOutputDevice(PIN_ADC_PWM, pin_factory=factory, frequency=5000)
setPointIDevice = DigitalInputDevice(PIN_SET_POINT_CMPR)
ctrlTempIDevice = DigitalInputDevice(PIN_CTRL_SNSR_CMPR)
alarmODevice = PWMOutputDevice(PIN_ALARM_PWM, frequency=10000)
alarmODevice.value = 0.8

def snoozeHandler(self):
    print("PRESSED!")

snoozeButton = gpiozero.Button(PIN_PREHEAT_BTN) 
snoozeButton.when_pressed = snoozeHandler

preheatLedODevice = DigitalOutputDevice(PIN_HEAT_CTRL)

probePowerDevice = DigitalOutputDevice(PIN_PROBE_POWER, initial_value=True)

def findProbe():
    # get list of current devices
    file_suffix = '/w1_slave'
    base_dir = '/sys/bus/w1/devices/'
    
    device_folders_before = glob.glob(base_dir + '28*')

    print(device_folders_before)

    if len(device_folders_before) == 0:
      return -1

    # turn off power to probe
    probePowerDevice.off()
    time.sleep(2)

    # get list of devices now
    device_folders_after = glob.glob(base_dir + '28*')
    print(device_folders_after)
    diff = list(set(device_folders_before) - set(device_folders_after))

    if (diff != 1):
      print("PROBE FINDING ERROR")
      return -1

    probePowerDevice.on()
    # return the difference
    return diff[0].split('/')[-1]

while(1):
    print(findProbe())
    time.sleep(3)
    #print("FINAL:", read_ADC_sensors_binary())
    #comparator_test()
    #alarmODevice.on()

    


