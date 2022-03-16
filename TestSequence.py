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
from ast import parse
from enum import Enum
from colorama import Fore, Style

from config import *
import time
import sys

import gpiozero
from gpiozero.output_devices import DigitalOutputDevice, PWMOutputDevice
from gpiozero.pins.mock import MockFactory
from gpiozero import DigitalInputDevice
from gpiozero import Device
# from gpiozero.pins.pigpio import PiGPIOFactory

# Hold results
test_results = dict()

# Possible responses: y (yes), n (no), s (skip), d (done), numerical value
def handleResponse(query, test, options, ADC=0, expected=None):
    r = None
    if (options == "i"):
        r = input(query + " (numerical value): ")
    else:
        r = input(query + " ({}): ".format(options))
        if (r not in options.split("/")):
            print("Invalid option. Must use ({})".format(options))

    if r == 's':
        return

    if (options == "y/n"):
        test_results[test] = (r, r == "y")
    elif (options == "d"):
        if (ADC):
            adc_value = 3.12 # read_ADC(ADC)
            test_results[test] = (adc_value,  expected[0] <= adc_value <= expected[1])
        else:
            device_value = device.value()
            test_results[test] = (device_value, device_value == expected)
            print(test_results)
    elif (options == "i"):
        test_results[test] = (r, expected[0] <= float(r) <= expected[1])
        print(test_results)

class Test(Enum):
    ALARM_LED = 0
    PREHEAT_LED = 1
    HEATER_COMMAND = 2
    ALARM_SOUND = 3
    BEGIN_READ = 4
    THERM_IN = 5
    THERM_OUT = 6
    MODE_SWITCH = 7
    PREHEAT_BTN = 8
    SNOOZE_BTN = 9
    HEATER_CHECK_1 = 10
    HEATER_CHECK_2 = 11
    HEATER_CHECK_3 = 12
    HEATER_CHECK_4 = 13
    ADC_BEGIN = 14
    ADC_POT = 15
    ADC_PORT0 = 16 
    ADC_PORT1 = 17
    ADC_BATTERY = 19
    END = 20

# Set factory for PC DEV
factory = MockFactory()
Device.pin_factory = factory

# Set up argparsing for state jumping
parser = argparse.ArgumentParser()
parser.add_argument('--test', type=str, required=False) # execute a single test 
parser.add_argument('--begin', type=str, required=False) # start at a certain certain test 
parser.add_argument('--end', type=str, required=False) # end at a certain test 

args = parser.parse_args()

end_bound = None
begin_bound = None
test_single = None

if (args.end):
    end_bound = Test[args.end]
if (args.begin):
    begin_bound = Test[args.begin]
if (args.test):
    test_single = Test[args.test]
    

device = None
state = Test(0)


if test_single:
    state = test_single
elif begin_bound:
    state = begin_bound

# Push button states and handlers
ph_pressed = False
snz_pressed = False
def ph_handler():
    ph_pressed = True
def snz_handler():
    snz_pressed = True



def process_output():
    print("{:<18} {:<8} {:<10}".format("TEST", "RESULT", "PASS/FAIL"))
    for k, v in test_results.items():
        print(Style.RESET_ALL, end = '') 
        color = Fore.GREEN if v[1] else Fore.RED
        print ("{:<18} {:<8}".format(k, v[0]) + color + " {:<10}".format("PASS" if v[1] else "FAIL"))
        print(Style.RESET_ALL, end = '') 


# Begin testing
while (1):

    # handle state bounds here
    if test_single and state != Test(test_single):
        break

    if end_bound and state.value > end_bound.value:
        break

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
            handleResponse("What is the voltage across the heating resistors?", "HEATER_LINE.ON", "i", expected=(10,13))
            time.sleep(0.1)
            print("Turning heater off...")
            device.off()
            handleResponse("What is the voltage across the heating resistors?", "HEATER_LINE.OFF", "i", expected=(0,2))
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
            device = DigitalInputDevice(PIN_THERM_IN)
            handleResponse("Write 0V to the Temperature Failsafe In (THERM_IN) line: ", "THERM_IN.LOW", "d", expected=0)
            handleResponse("Write 3.3V to the Temperature Failsafe In (THERM_IN) line: ", "THERM_IN.HIGH", "d", expected=1)
            state = Test(state.value + 1)

        elif (state == Test.THERM_OUT):
            device = DigitalInputDevice(PIN_THERM_OUT)
            handleResponse("Write 0V to the Temperature Failsafe Out (THERM_OUT) line: ", "THERM_OUT.LOW", "d", expected=0)
            handleResponse("Write 3.3V to the Temperature Failsafe In (THERM_OUT) line: ", "THERM_OUT.HIGH", "d", expected=1)
            state = Test(state.value + 1)

        elif (state == Test.MODE_SWITCH):
            device = DigitalInputDevice(PIN_MODE_SWITCH)
            handleResponse("Flip the system to baby mode: ", "MODE_SWITCH.BABY", "d", expected=0)
            device = DigitalInputDevice(PIN_MODE_SWITCH)
            handleResponse("Flip the system to air mode: ", "MODE_SWITCH.AIR", "d", expected=1)
            state = Test(state.value + 1)

        elif (state == Test.PREHEAT_BTN):
            ph_btn = gpiozero.Button(PIN_PREHEAT_BTN)
            ph_btn.when_pressed = ph_handler
            t = input("Press the preheat button within 10 seconds. Input 's' to skip or any other key to begin: ")
            if (t == 's'):
                state = Test(state.value + 1)
                continue
            btime = time.time()
            while ((time.time() - btime < 10) and not ph_pressed):
                time.sleep(0.1)
            print("PRESS DETECTED") if ph_pressed else print("PRESS NOT DETECTED")
            test_results["PREHEAT_BTN.ACTIVATE"] = (ph_pressed, ph_pressed)
            state = Test(state.value + 1)

        elif (state == Test.SNOOZE_BTN):
            snz_btn = gpiozero.Button(PIN_SNOOZE_BTN)
            snz_btn.when_pressed = snz_handler
            t = input("Press the snooze button within 10 seconds. Input 's' to skip or any other key to begin: ")
            if (t == 's'):
                state = Test(state.value + 1)
                continue
            btime = time.time()
            while ((time.time() - btime < 10) and not snz_pressed):
                time.sleep(0.1)
            print("PRESS DETECTED") if snz_pressed else print("PRESS NOT DETECTED")
            test_results["PREHEAT_BTN.ACTIVATE"] = (snz_pressed, snz_pressed)
            state = Test(state.value + 1)
            
        elif (state == Test.HEATER_CHECK_1):
            device = DigitalInputDevice(PIN_HEATER_CHECK_1)
            handleResponse("Write 3.3V to the Heater Check 1 line: ", "HEATER_CHECK1.HIGH", "d", expected=1 )
            handleResponse("Write 0V to the Heater Check 1 line: ", "HEATER_CHECK1.LOW", "d", expected=0)
            state = Test(state.value + 1)   

        elif (state == Test.HEATER_CHECK_2):
            device = DigitalInputDevice(PIN_HEATER_CHECK_2)
            handleResponse("Write 3.3V to the Heater Check 2 line: ", "HEATER_CHECK2.HIGH", "d", expected=1)
            handleResponse("Write 0V to the Heater Check 2 line: ", "HEATER_CHECK2.LOW", "d", expected=0)
            state = Test(state.value + 1)

        elif (state == Test.HEATER_CHECK_3):
            device = DigitalInputDevice(PIN_HEATER_CHECK_3)
            handleResponse("Write 3.3V to the Heater Check 3 line: ", "HEATER_CHECK3.HIGH", "d", expected=1)
            handleResponse("Write 0V to the Heater Check 3 line: ", "HEATER_CHECK3.LOW", "d", expected=1)
            state = Test(state.value + 1)   

        elif (state == Test.HEATER_CHECK_4):
            device = DigitalInputDevice(PIN_HEATER_CHECK_4)
            handleResponse("Write 3.3V to the Heater Check 4 line: ", "HEATER_CHECK4.HIGH", "d", expected=1)
            handleResponse("Write 0V to the Heater Check 5 line: ", "HEATER_CHECK4.LOW", "d", expected=0)
            state = Test(state.value + 1)   

        elif (state == Test.ADC_BEGIN):
            print("\nNow prepare to test the ADCs. Prepare a powersupply to write to the temperatures sensor ports or lines.")
            state = Test(state.value + 1)

        elif (state == Test.ADC_POT):
            handleResponse("Spin the temperature control knob to the lowest bound.", "ADC_POT.LOW", "d", 1, expected=(0.38, 0.41))
            handleResponse("Spin the temperature control knob to the highest bound.", "ADC_POT.HIGH", "d", 1, expected=(0.28, 0.31))
            state = Test(state.value + 1)
            
        elif (state == Test.ADC_PORT0):
            handleResponse("Drive the temperature sensor port (0) to 0V.", "ADC_PORT0.0", "d", 2, expected=(0.0, 0.03) )
            handleResponse("Drive the temperature sensor port (0) to 3V.", "ADC_PORT0.3", "d", 2, expected=(2.9, 3.1))
            handleResponse("Drive the temperature sensor port (0) to 0.3V.", "ADC_PORT0.03", "d", 2, expected=(0.29, 0.31))
            handleResponse("Drive the temperature sensor port (0) to 0.4V.", "ADC_PORT0.04", "d", 2, expected=(0.39, 0.41))
            handleResponse("Drive the temperature sensor port (0) to 0.31V.", "ADC_PORT0.031", "d", 2, expected=(0.29, 0.31))
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
            process_output()
            break
    except KeyboardInterrupt:
        print(" Force quit...")
        process_output()
        sys.exit()

print(test_results)







