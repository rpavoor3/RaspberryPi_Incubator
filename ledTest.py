import RPi.GPIO as GPIO
import time
pin1= 18 #red seperate
pin2= 17 
pin3= 27
pin4 = 22
switch = 10

GPIO.setmode(GPIO.BOARD)
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(pin1,GPIO.OUT)
#GPIO.setup(pin2,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
#GPIO.setup(13,GPIO.OUT)
GPIO.setup(switch,GPIO.IN,pull_up_down=GPIO.PUD_UP)

while(1):
    #print(GPIO.input(switch),'\n')
    #if GPIO.input(switch):
        GPIO.output(11,GPIO.HIGH)
        #GPIO.output(15,GPIO.HIGH)
        time.sleep(2)
        GPIO.output(11,GPIO.LOW)
        #GPIO.output(15,GPIO.LOW)
        time.sleep(2)
        
 
        
        """
        GPIO.output(pin2,GPIO.HIGH)
        time.sleep(2)
        GPIO.output(pin3,GPIO.HIGH)
        time.sleep(2)
        GPIO.output(pin4,GPIO.HIGH)"""




