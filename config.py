
from tkinter.constants import TRUE


PC_DEV = True

"""
Monitor Details
"""

BG_COLOR = 'black'          # Background Color
FONT_COLOR = 'white'        # changes color of all text
TIMEZONE = 'US/Eastern'     # set timezone Replace with 'Africa/Accra'

"""
Pin Assignments
"""

# ambient temp not explicitly written DTMP_PI = 21
PIN_SNOOZE_BTN = 3 #5               # Snooze Button
PIN_ALARM_LED = 16 #36
PIN_PREHEAT_BTN = 2 #3
PIN_PREHEAT_LED = 21 #40
PIN_HEATER_CHECK_1 = 13 #33
PIN_HEATER_CHECK_2 = 6 #31
PIN_HEATER_CHECK_3 = 5 #29
PIN_HEATER_CHECK_4 = 22 #15
PIN_THERM_IN = 26 #37
PIN_THERM_OUT = 27 #13
PIN_SET_POINT_CMPR = 18 #12
PIN_ALARM_PWM = 19 #35
PIN_ADC_SOURCE = 12 #32
PIN_HEAT_CTRL = 4 #7
PIN_MODE_SWITCH = 17 #11
PIN_BATTERY_LEVEL = 23 #16
PIN_BABY_TEMP = 24 #18
PIN_AIR_TEMP = 25 #22
PIN_REF_HI = 8 #24
PIN_REF_LO = 7 #26
PIN_FAULT_LED = 20 #38
PIN_BATTERY_RELAY = -1

# Taken to ground
# gpio: 14, 15, 28, 10, 9, 11, 

"""
Skin Temperature Settings in Sensor.py
"""
DIGITAL_VOLTAGE = 3.3

# PWM Settings
ADC_VOLTAGE_LOWER = 0.20   # starting range for skin temperature
ADC_VOLTAGE_UPPER = 0.45   # Ending range for skin temperature
ADC_SEARCH_CYCLES = 7


ADC_START_VOLTAGE = 0.20
ADC_END_VOLTAGE = 0.45

# Warning Settings
SKIN_TEMP_THRES_MAX = 39    # Minimum Skin Temperature Threshold Value
SKIN_TEMP_THRES_MIN = 20    # Maximum Skin Temperature Threshold Value
#TODO: these values need to be double checked
AMB_TEMP_THRES_MIN = 30     # Minimum Ambient(Incubator) Temperture Threshold Value
AMB_TEMP_THRES_MAX = 40     # Maximum Ambient(Incubator) Temperture Threshold Value
CONTROL_THRESHOLD = 0.5
ALARM_THRESHOLD = 2


"""
Speaker Settings
"""

SPKR_FREQ = 2000            # Frequency of the speaker sound
SNOOZE_LENGTH = 120         # Indicates how long the snooze button should last (in seconds)

