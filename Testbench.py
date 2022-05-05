import argparse
import time
from tracemalloc import start
from config import *
import itertools, sys


import gpiozero
from gpiozero.output_devices import DigitalOutputDevice, PWMOutputDevice
from gpiozero.pins.mock import MockFactory
from gpiozero import DigitalInputDevice
from gpiozero import Device
from gpiozero.pins.pigpio import PiGPIOFactory

# THis is the code that will test whether the pi is set up correctly
# It will also provide a command interface to test individual components

spinner = itertools.cycle(['-', '/', '|', '\\'])

def spin():
    while True:
        sys.stdout.write(next(spinner))   # write the next character
        sys.stdout.flush()                # flush stdout buffer (actual character display)
        sys.stdout.write('\b')            # erase the last written char

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    quit()

parser = argparse.ArgumentParser()

parser.add_argument('--type', type=str, required=True) # write, read, test
parser.add_argument('--target', type=str, required=True) # alarm_led, switch, ADC, etc
parser.add_argument('--command', type=str, required=False) # LOW, HIGH, etc

args = parser.parse_args()

# Device acquisition
device = None

if args.type == "WRITE":
    if args.target == "ALARM_LED":
        device = DigitalOutputDevice(PIN_ALARM_LED)
    elif args.target == "DIGITAL_HEAT":
        device = DigitalOutputDevice(PIN_HEAT_CTRL)
    elif args.target == "PREHEAT_LED":
        device = DigitalOutputDevice(PIN_PREHEAT_LED)
    elif args.target == "FAULT_LED":
        device = DigitalOutputDevice(PIN_FAULT_LED)
    else:
        eprint("Invalid target for WRITE")

    if (args.command == "LOW"):
        device.off()
    if (args.command == "HIGH"):
        device.on()
    if (args.command == "TRISTATE"):
        device.close()

    print ("Setting {} to {} ...".format(args.target, args.command))
    spin()

if args.type == "READ":
    if args.target == "THERM_IN":
        device = DigitalInputDevice(PIN_THERM_IN)
    elif args.target == "THERM_OUT":
        device = DigitalInputDevice(PIN_THERM_OUT)
    elif args.target == "MODE_SWITCH":
        device = DigitalInputDevice(PIN_MODE_SWITCH)
    elif args.target == "BATTERY_RELAY":
        device = DigitalInputDevice(PIN_BATTERY_RELAY)
    elif args.target == "PREHEAT_BTN":
        device = DigitalInputDevice(PIN_PREHEAT_BTN, pull_up=True)
    elif args.target == "SNOOZE_BTN":
        device = DigitalInputDevice(PIN_SNOOZE_BTN, pull_up=True)
    elif args.target == "HEATER_TEST_1":
        device = DigitalInputDevice(PIN_HEATER_CHECK_1)
    elif args.target == "HEATER_TEST_2":
        device = DigitalInputDevice(PIN_HEATER_CHECK_2)
    elif args.target == "HEATER_TEST_3":
        device = DigitalInputDevice(PIN_HEATER_CHECK_3)
    elif args.target == "HEATER_TEST_4":
        device = DigitalInputDevice(PIN_HEATER_CHECK_4)
    else:
        eprint("Invalid target for READ")

    print("Reading state of {} ...".format(args.target))
    start_time = time.time()
    while (1):
        print("{}: {}".format(time.time()-start_time, device.value))
        time.sleep(0.5)

# Excute command or test

if (args.type == "TEST"):

    # ADC
    if args.target == "ADC":
        print("testing ADCs")
        print("Pot, Air, Baby, Battery")

    elif args.target == "ALARM_SPEAKER":
        device = PWMOutputDevice(PIN_ALARM_PWM)
        if (args.command == "ON"):
            device.frequency(2000)
            device.on()
        elif (args.command == "OFF"):
            device.off()
        else:
            eprint("Need to specify command for alarm speaker.")
        spin()

