import gpiozero
from gpiozero import Device
from gpiozero import DigitalInputDevice
from gpiozero.output_devices import DigitalOutputDevice, PWMOutputDevice
from gpiozero.pins.pigpio import PiGPIOFactory
import time 
import glob

#from gpiozero.pins.mock import MockFactory, MockPWMPin
#Device.pin_factory = MockFactory(pin_class=MockPWMPin)
factory = PiGPIOFactory()

test = DigitalInputDevice(8, pin_factory=factory)

def read_digital_sensors(self):

    file_suffix = '/w1_slave'
    base_dir = '/sys/bus/w1/devices/'
    device_folders = glob.glob(base_dir + '28*')

    result_dict = dict()

    for d_f in device_folders:
        device_file = d_f + file_suffix
        serial_id = d_f.split('/')[-1]
        lines = self.read_digital_temp_raw(device_file)
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_digital_temp_raw(device_file)
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            result_dict[serial_id] = temp_c

    return result_dict 

while (True):
    print(read_digital_sensors())
    time.sleep(0.5)