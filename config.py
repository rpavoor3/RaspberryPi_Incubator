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
PIN_PWM_PI = 13             # Comparator PWM
PIN_ALARM_PWM = 10          # Speaker
PIN_BATT_OFF = 22           # Power Source
PIN_ADC1_OUT = 6            # Setpoint (User Reading)
PIN_ADC2_OUT = 19           # Temperature
PIN_PI_HEAT = 26            # Digital Temperature Control TODO
PIN_LED1 = 16               # Red
PIN_LED2 = 12               # Orange/Yellow
PIN_LED3 = 1                # Green
PIN_LED4 = 7                # Blue

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

"""
Speaker Settings
"""

SPKR_FREQ = 2000            # Frequency of the speaker sound
