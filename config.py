
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
PIN_MUTE = 21               # Snooze Button
PIN_ADC_PWM = 18             # Comparator PWM
PIN_ALARM_PWM = 24          # Speaker
PIN_BATT_OFF = 22           # Power Source
PIN_ADC1_CMPR = 6            # Setpoint (User Reading)
PIN_ADC2_CMPR = 19           # Temperature
PIN_PI_HEAT = 26            # Digital Temperature Control TODO
PIN_LED1 = 16               # Red
PIN_LED2 = 12               # Orange/Yellow
# TODO: PIN_LED3 is actually pointing to pin 1 on the PCB but this needs to be changed
PIN_LED3 = 5                # Green
PIN_LED4 = 7                # Blue

PIN_POWER = 22              # Indicates whether or not the power is connected to main power or backup power


"""
Skin Temperature Settings in Sensor.py
"""
# PWM Settings
ADC_START_VOLTAGE = 200000  # starting range for skin temperature
ADC_END_VOLTAGE = 1000000   # Ending range for skin temperature
ADC_STEP = 1000             # Number of steps
# Warning Settings
SKIN_TEMP_THRES_MAX = 39    # Minimum Skin Temperature Threshold Value
SKIN_TEMP_THRES_MIN = 20    # Maximum Skin Temperature Threshold Value
#TODO: these values need to be double checked
AMB_TEMP_THRES_MIN = 30     # Minimum Ambient(Incubator) Temperture Threshold Value
AMB_TEMP_THRES_MAX = 40     # Maximum Ambient(Incubator) Temperture Threshold Value


"""
Speaker Settings
"""

SPKR_FREQ = 2000            # Frequency of the speaker sound
SNOOZE_LENGTH = 120         # Indicates how long the snooze button should last (in seconds)

