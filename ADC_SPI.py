from gpiozero import MCP3002
from time import sleep

adc = MCP3002(channel=0, clock_pin=21, mosi_pin=20, miso_pin=19, select_pin=16)

while(1):
    data = adc.value
    print(data)
    sleep(0.5)

