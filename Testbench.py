from gpiozero import DigitalOutputDevice
from gpiozero.pins.pigpio import PiGPIOFactory
import time

x = DigitalOutputDevice(26)

while(1):
    x.on()
    time.sleep(1)
    print("Running...")
