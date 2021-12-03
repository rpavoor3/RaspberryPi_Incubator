import gpiozero
from gpiozero import Device
from gpiozero import DigitalInputDevice
from gpiozero.output_devices import DigitalOutputDevice, PWMOutputDevice

#from gpiozero.pins.mock import MockFactory, MockPWMPin
#Device.pin_factory = MockFactory(pin_class=MockPWMPin)
factory = PiGPIOFactory()

test = DigitalInputDevice(8, pin_factory=factory)

print("done")