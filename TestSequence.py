# TestSequence.py
#
# - This script will preform a guided test to execute a sainity test
# on the various peripherals of a fully constructed and wired incubator
# - The output of this script is a test summary based on user inputs and
# detected state
#
# Author: Hussain Miyaziwala
# Date: 3/3/2022

import argparse
from enum import Enum

from config import *
import time
import sys

import gpiozero
from gpiozero.output_devices import DigitalOutputDevice, PWMOutputDevice
from gpiozero.pins.mock import MockFactory
from gpiozero import DigitalInputDevice
from gpiozero import Device
from gpiozero.pins.pigpio import PiGPIOFactory

# Hold results
test_results = dict()

# Possible responses: y (yes), n (no), s (skip), d (done), numerical value
def handleResponse(query, test, options, ADC=0):
    while (1):

        if (options == "i"):
            r = input(query + " (numerical value): ")
            if r == 's':
                return
            test_results[test] = r
            return

        r = input(query + " ({}): ".format(options))
        if (r == "s"):
            return
        if (r not in options.split("/")):
            print("Invalid option. Must use ({})".format(options))
        else:
            if (options == "d"):
                if (ADC):
                    test_results[test] = 3.12 #read actual adc value here
                else:
                    test_results[test] = device.value()
            else:
                test_results[test] = r
            return

class Test(Enum):
    ALARM_LED = 0
    PREHEAT_LED = 1
    HEATER_COMMAND = 2

    END = 3

# Set factory for PC DEV
factory = MockFactory()
Device.pin_factory = factory

# Set up argparsing for state jumping
parser = argparse.ArgumentParser()
parser.add_argument('--test', type=str, required=False) # jump to certain test 
parser.add_argument('--begin', type=str, required=False) # start at a certain certain test 
parser.add_argument('--end', type=str, required=False) # end at a certain test 


# Ideation for Steps:
'''

1. Set up device properties, import libraries, create tags
2. create framework for statemachine and input reading (press y/n if correct or incorrect)
3. Capture results and report as we go 

'''

device = None
state = Test.ALARM_LED

# Begin testing

while (1):
    try:
        if (state == Test.ALARM_LED):
            device = DigitalOutputDevice(PIN_ALARM_LED)
            device.on()
            handleResponse("Is the Alarm LED on?", "ALARM_LED.ON", "y/n")
            time.sleep(0.1)
            device.off()
            handleResponse("Is the Alarm LED off?", "ALARM_LED.OFF", "y/n")
            state = Test(state.value + 1)

        elif (state == Test.PREHEAT_LED):
            device = DigitalOutputDevice(PIN_PREHEAT_LED)
            device.on()
            handleResponse("Is the Preheat LED on?", "PREHEAT_LED.ON", "y/n")
            time.sleep(0.1)
            device.off()
            handleResponse("Is the Preheat LED off?", "PREHEAT_LED.OFF", "y/n")
            state = Test(state.value + 1)

        elif (state == Test.HEATER_COMMAND):
            device = DigitalOutputDevice(PIN_HEAT_CTRL)
            t = input("Enter 's' to skip the heater test, otherwise enter any key to continue:")
            if (t == 's'):
                state = Test(state.value + 1)
                continue
            print("Turning heater on...")
            device.on()
            handleResponse("What is the voltage across the power resistors?", "HEATER_LINE.ON", "i")
            time.sleep(0.1)
            print("Turning heater off...")
            device.off()
            handleResponse("What is the voltage across the power resistors?", "HEATER_LINE.OFF", "i")
            state = Test(state.value + 1)

        elif (state == Test.ALARM_SOUND):
            device = PWMOutputDevice(PIN_ALARM_PWM)
            device.frequency(2000)
            device.on()
            handleResponse("Can you hear a single tone?", "ALARM_SOUND.ON", "y/n")
            device.off()
            handleResponse("Did the tone turn off?", "ALARM_SOUND.OFF", "y/n")
            state = Test(state.value + 1)
    
        elif (state == Test.BEGIN_READ):
            print("\nNow prepare a powersupply to write to the various input lines of the incubator.")
            state = Test(state.value + 1)

        elif (state == Test.THERM_IN):
            device = DigitalOutputDevice(PIN_THERM_IN)
            handleResponse("Write 0V to the Temperature Failsafe In (THERM_IN) line: ", "THERM_IN.LOW", "d")
            device = DigitalOutputDevice(PIN_THERM_IN)
            handleResponse("Write 3.3V to the Temperature Failsafe In (THERM_IN) line: ", "THERM_IN.HIGH", "d")
            state = Test(state.value + 1)

        elif (state == Test.THERM_OUT):
            device = DigitalOutputDevice(PIN_THERM_OUT)
            handleResponse("Write 0V to the Temperature Failsafe Out (THERM_OUT) line: ", "THERM_OUT.LOW", "d")
            device = DigitalOutputDevice(PIN_THERM_OUT)
            handleResponse("Write 3.3V to the Temperature Failsafe In (THERM_OUT) line: ", "THERM_OUT.HIGH", "d")
            state = Test(state.value + 1)

        # TODO: Complete inserting remainder of reading tests... Ruth, wanna help? :)

        elif (state == Test.ADC_BEGIN):
            print("\nNow prepare to test the ADCs. Prepare a powersupply to write to the temperatures sensor ports or lines.")
            state = Test(state.value + 1)

        elif (state == Test.ADC_POT):
            handleResponse("Spin the temperature control knob to the lowest bound.", "ADC_POT.LOW", "d", 1)
            handleResponse("Spin the temperature control knob to the highest bound.", "ADC_POT.HIGH", "d", 1)
            state = Test(state.value + 1)
            
        elif (state == Test.ADC_PORT0):
            handleResponse("Drive the temperature sensor port (0) to 0V.", "ADC_PORT0.0", "d", 2)
            handleResponse("Drive the temperature sensor port (0) to 3V.", "ADC_PORT0.3", "d", 2)
            handleResponse("Drive the temperature sensor port (0) to 0.3V.", "ADC_PORT0.03", "d", 2)
            handleResponse("Drive the temperature sensor port (0) to 0.4V.", "ADC_PORT0.04", "d", 2)
            handleResponse("Drive the temperature sensor port (0) to 0.31V.", "ADC_PORT0.031", "d", 2)
            state = Test(state.value + 1)
        
        elif (state == Test.ADC_PORT1):
            handleResponse("Drive the temperature sensor port (1) to 0V.", "ADC_PORT1.0", "d", 3)
            handleResponse("Drive the temperature sensor port (1) to 3V.", "ADC_PORT1.3", "d", 3)
            handleResponse("Drive the temperature sensor port (1) to 0.3V.", "ADC_PORT1.03", "d", 3)
            handleResponse("Drive the temperature sensor port (1) to 0.4V.", "ADC_PORT1.04", "d", 3)
            handleResponse("Drive the temperature sensor port (1) to 0.31V.", "ADC_PORT1.031", "d", 3)
            state = Test(state.value + 1)

        elif (state == Test.ADC_BATTERY):
            handleResponse("Drive the battery voltage reader line to 0V.", "ADC_BATTERY.0", "d", 4)
            handleResponse("Drive the battery voltage reader line to 12V.", "ADC_BATTERY.12", "d", 4)
            handleResponse("Drive the battery voltage reader line to 10V.", "ADC_BATTERY.10", "d", 4)
            handleResponse("Drive the battery voltage reader line to 8V.", "ADC_BATTERY.8", "d", 4)
            handleResponse("Drive the battery voltage reader line to 4V.", "ADC_BATTERY.4", "d", 4)
            state = Test(state.value + 1)
    

        else:
            print("Test Complete")
            # processOutput()
            break
    except KeyboardInterrupt:
        print("Force exit")
        # procesOutput()
        sys.exit()

print(test_results)







