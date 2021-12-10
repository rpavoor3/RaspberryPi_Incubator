from tkinter import *
from config import *
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
alarmODevice = PWMOutputDevice(PIN_ALARM_PWM, frequency=2000)
while(1):
    time.sleep(1)
    #print("FINAL:", read_ADC_sensors_binary())
    #comparator_test()
    alarmODevice.on()

    


