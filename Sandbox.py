import gpiozero
from gpiozero import Device
from gpiozero.output_devices import DigitalOutputDevice, PWMOutputDevice

from gpiozero.pins.mock import MockFactory, MockPWMPin
Device.pin_factory = MockFactory(pin_class=MockPWMPin)

adc = PWMOutputDevice(13)

adc.value = 1

print("Running")

while(True):
    adc.value = 1