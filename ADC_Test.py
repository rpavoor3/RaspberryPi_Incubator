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
    
low = ADC_START_VOLTAGE
high = ADC_END_VOLTAGE
lower_limit = ADC_VOLTAGE_LOWER
upper_limit = ADC_VOLTAGE_UPPER

factory = PiGPIOFactory()

adcPwmODevice = PWMOutputDevice(PIN_ADC_PWM, pin_factory=factory)
adcPwmODevice.value = 0.5