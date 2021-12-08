from gpiozero import DigitalOutputDevice
from gpiozero.pins.pigpio import PiGPIOFactory
import time

x = DigitalOutputDevice(12)
x.on()

while(1): 
    time.sleep(1)
    print("Running...")