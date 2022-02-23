#!/usr/bin/python
#
# Copyright Whit Smith 2021
# 2021 June 5 rev 2
#
# Raspberry Pi SPI Output test
# Can PDM audio be sent via SPI?
#

import spidev
import time
import random
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
from statistics import pstdev
from statistics import mean
import math

# Constants
Vrefhi = 1021/1000  # Volts
Vreflo =  500/1000  # Volts
Vcc    = 3296/1000  # Volts
samples = 20        # Samples for statistical estimate


Vcc = Vcc * 100/(100+2.2) # Specific to 2.2k and 100k divider
# Clear all from a possibly prior run
# pins = [12, 13, 26, 21]
# GPIO.cleanup( pins )


GPIO.setmode(GPIO.BCM)   # use the port number, not the pin numbers

# Set these lines as input so not to fight the op-amp
GPIO.setup(12, GPIO.IN)
GPIO.setup(13, GPIO.IN)
GPIO.setup(26, GPIO.IN)

GPIO.setup(20, GPIO.IN)  # Later use this to ground RC
GPIO.setup(21, GPIO.OUT) # This is the output thru 2.2k

tref=[]
tsig1=[]
tsig2=[]
loopsum=0

# Really poor first shot using polling
# Replace with transition driven interrupt callbacks
t_sampling = time.time()
for i in range(samples):
    # Charge up RC Capacitor
    #print("P21 = 3.3V")
    GPIO.setup( 21, GPIO.OUT)
    GPIO.output(21, GPIO.HIGH)
    time.sleep(0.05)
    
    # Prepare to disconnect P21
    t12=0
    t13=0
    t26=0
    #print("P21 = Input = Hi-Z")
    
    # Disconnect P21
    GPIO.setup( 21, GPIO.IN)
    t0=time.time()                # Get timestamp
    
    # While
    #  Any GPIO still is HI
    #   and
    #  Not timed out yet
    loops = 0
    while( ((t12==0) or (t13==0) or (t26==0)) and ((time.time()-t0)<4.0)):
        
        loops +=1            # Count loops
        
        if(t12==0):
            if( GPIO.input(12)==GPIO.LOW ):
                t12=time.time()-t0
        
        if(t13==0):
            if( GPIO.input(13)==GPIO.LOW ):
                t13=time.time()-t0
        
        if(t26==0):
            if( GPIO.input(26)==GPIO.LOW ):
                t26=time.time()-t0

    #print("GPIO transition test loops=", loops)
    #print("Sample=", i, " t12=", t12, " t13=", t13, " t26=", t26)
    tref.append(t12)
    tsig1.append(t13-t12)
    tsig2.append(t26-t12)
    loopsum += loops
    
t_sampling = time.time() - t_sampling


print("loops: mean=", loopsum/samples, "samples =", samples, " time/sample =", t_sampling/samples)
print(" tref: mean=", mean(tref),  " stdev=", pstdev(tref) )
print("tsig1: mean=", mean(tsig1), " stdev=", pstdev(tsig1))
print("tsig2: mean=", mean(tsig2), " stdev=", pstdev(tsig2))

import math

# Estimate RC and Vsig2 from Vcc and Vrefhi
# Not sure this is quite right
RC = -1 * mean(tref)/math.log(Vrefhi/Vcc)
Vsig2 = Vcc*math.exp(-1 * (mean(tsig2)+mean(tref))/RC)

print("Calculated: Vsig2=", Vsig2, "Volts,    RC=", RC, "Seconds  from Vcc and Vrefhi")


# Estimate RC and Vsig2
RC = -1 * mean(tsig1)/math.log(Vreflo/Vrefhi)
Vsig2 = Vrefhi*math.exp(-1 * mean(tsig2)/RC)

print("Calculated: Vsig2=", Vsig2, "Volts,    RC=", RC, "Seconds   from Vrefhi and Vreflo")

plt.plot(range(samples), tref,  label="tref")
plt.plot(range(samples), tsig1, label="tsig1")
plt.plot(range(samples), tsig2, label="tsig2")
plt.legend()
plt.show()
