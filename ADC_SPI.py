from gpiozero import MCP3002
from time import sleep

adc = MCP3002(channel=0)

while(1):
    # data = 100 * (adc.value * 5) - 50
    data = adc.value * 5
    print(data)
    sleep(1)

