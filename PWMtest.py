import pigpio
import time
from w1thermsensor import W1ThermSensor, Sensor

pi1 = pigpio.pi()

pi1.set_mode(6, pigpio.INPUT)# Temp Sensor
pi1.set_mode(26, pigpio.INPUT)# Setpoint
pi1.set_mode(24, pigpio.OUTPUT)# Speaker Tone

# set speaker PWM
pi1.set_PWM_dutycycle(24,128)
pi1.set_PWM_frequency(24,2000)

def skin_temperature():
    skin = -1
    spoint = -1
    for i in range(200000, 1000000, 1000):
        pi1.hardware_PWM(18, 100000, i) # PWM signal
        time.sleep(0.03)
        x = pi1.read(6)
        y = pi1.read(26)
        if(x == 1 and skin == -1):
            skin = i
            #print('skinTemp:',((3.3 * float(skin) / 1000000) - 0.5) * 100.0)
        if(y == 1 and spoint == -1):
            spoint = i
            #print('SetPoint:',((3.3 * float(spoint) / 1000000) - 0.5) * 100.0)
        if (x == 1 and y == 1):
            print('skinTemp:',((3.3 * float(skin) / 1000000) - 0.5) * 100.0)
            print('SetPoint:',((3.3 * float(spoint) / 1000000) - 0.5) * 100.0)
            break
        
def ambient_temp():
   # print("AT")
    for sensor in W1ThermSensor.get_available_sensors([Sensor.DS18B20]):
        print("AmbientTemp: {} reads {}".format(sensor.id, sensor.get_temperature()))    
while (1):
    skin_temperature()
    ambient_temp()
    time.sleep(0.2)
    