import pigpio
import time

pi1 = pigpio.pi()
"""
pi1.set_mode(6, pigpio.INPUT)
pi1.set_mode(26, pigpio.INPUT)


def temperature():
      
  for i in range(200000, 1000000, 1000):
      pi1.hardware_PWM(18, 100000, i)
      time.sleep(0.03)
      x = pi1.read(6)
      y = pi1.read(26)
      if(x == 1):
          print(((3.3 * float(i) / 1000000) - 0.5) * 100.0)
          print(((3.3 * float(i) / 1000000)))
          break
    

while (1):
    temperature()
    time.sleep(0.2)
"""
pi1.set_mode(24, pigpio.OUTPUT)
pi1.set_PWM_dutycycle(24,50)
pi1.set_PWM_frequency(24,2000)