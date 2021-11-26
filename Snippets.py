
# Read Digital Temperature Sensors
https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing?view=all 

import glob
import time

file_suffix = '/w1_slave'
base_dir = '/sys/bus/w1/devices/'

def read_temp_raw(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def get_temperature_readings():

    # Can make this global if we think devices wont change for given use.
    device_folders = glob.glob(base_dir + '28*')

    result_dict = dict()

    for d_f in device_folders:
        device_file = d_f + file_suffix
        lines = read_temp_raw(device_file)
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw(device_file)
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            result_dict[d_f] = [temp_f, temp_c]

    return result_dict # could make generator here

# Set One Wire
https://pinout.xyz/pinout/1_wire 

# Controller Code
if heating && temperature > setpoint + ctrl_threshold:
    stop_heating
if not heating && tempearture < setpoint - ctrl_threshold:
    start_heating

# Push button pressed

# Snooze

from gpiozero import Button
from signal import pause

def snooze_handler():
    # snooze = on
    # feed snooze timer
    end

snooze_button = Button(2)
snooze_button.when_pressed = snooze_handler

pause() # keeps async scripts running, will not need given base while loop


# Preheat
from gpiozero import Button
from signal import pause

def preheat_handler():
    # toggle preheat ->
    preheat_status = not preheat_status

preheat_button = Button(2)

preheat_button.when_pressed = preheat_handler


# ADC Reading Code
pwm_device = PWMOutputDevice(ADC_pin)
adc_comp = DigitalInputDevice(comparator_pin)

for i in range(ADC_START_VOLTAGE, ADC_END_VOLTAGE, ADC_STEP):
    pwm_device.value(i / voltage_conversion ) #value needs to be [0,1]

    # read the comparator status
    if adc_comp.value() == 1:
        #you found the thing, handle accordingly
        end
    

# Mock Factory
from gpiozero import Device
from gpiozero.pins.mock import MockFactory

Device.pin_factory = MockFactory()

    # you can now create devices ad hock

#RPIO Factory
from gpiozero.pins.rpio import RPIOFactory
from gpiozero import LED

factory = RPIOFactory()
led = LED(12, pin_factory=factory)