"""
Monitor Details
"""

bg_color = 'black'          # Background Color
font_color = 'white'        # changes color of all text
timezone = 'US/Eastern'     # set timezone Replace with 'Africa/Accra'

"""
Pin Assignments
"""

# ambient temp not explicitly written DTMP_PI = 21
pin_MUTE = 21               # Snooze Button
pin_PWM_PI = 13             # Comparator PWM
pin_ALARM_PWM = 10          # Speaker
pin_BATT_OFF = 22           # Power Source
pin_ADC1_OUT = 6            # Setpoint (User Reading)
pin_ADC2_OUT = 19           # Temperature
pin_PI_HEAT = 26            # Digital Temperature Control
pin_LED1 = 16               # Red
pin_LED2 = 12               # Orange/Yellow
pin_LED3 = 1                # Green
pin_LED4 = 7                # Blue

"""
Skin Temperature Settings in Sensor.py
"""
# PWM Settings
ADC_start_voltage = 200000  # starting range for skin temperature
ADC_end_voltage = 1000000   # Ending range for skin temperature
ADC_step = 1000             # Number of steps
# Warning Settings
skin_temp_thres_max = 39    # Minimum Skin Temperature Threshold Value
skin_temp_thres_min = 20    # Maximum Skin Temperature Threshold Value

"""
Speaker Settings
"""

spkr_freq = 2000            # Frequency of the speaker sound
