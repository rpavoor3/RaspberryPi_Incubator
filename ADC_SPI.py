from gpiozero import MCP3002
from time import sleep

adc = MCP3002(channel=0)


while(1):
    print(adc.value * 5)
    sleep(0.5)

