import pigpio
import time
import random
import matplotlib.pyplot as plt
from statistics import pstdev
from statistics import mean
import math


# pins 
adc_ref_1 = pin24, 1.2v
adc_ref_2 = pin26, 0.6v
read = 3rd pin

# Constants
Vrefhi = 1021/1000  # Volts
Vreflo =  500/1000  # Volts
Vcc    = 3297/1000  # Volts
samples = 200        # Samples for statistical estimate

t0 = 0
tlo = 0
thi = 0
t26 = 0

def cbf_lo(event, level, tick):
    # print("Tick from lo", tick)
    if (globals()['tlo'] == 0):
        globals()['tlo']  = tick - globals()['t0'] 

def cbf_hi(event, level, tick):
    # print("Tick from hi", tick)
    if (globals()['thi']  == 0):
        globals()['thi']  = tick - globals()['t0'] 
        
def cbf_26(event, level, tick):
    # print("Tick from 26", tick)
    if (globals()['t26']  == 0):
        globals()['t26']  = tick - globals()['t0'] 

def init(pi, p1, p2, p3, p4, o1):

    pi.set_mode(p1, pigpio.INPUT)
    pi.set_mode(p2, pigpio.INPUT)
    pi.set_mode(p3, pigpio.INPUT)

    pi.set_mode(p4, pigpio.INPUT) # Later use this to ground RC
    pi.set_mode(o1, pigpio.OUTPUT) # This is the output thru 2.2k
    
    cblo = pi.callback(p1, pigpio.FALLING_EDGE, cbf_lo)
    cbhi = pi.callback(p2, pigpio.FALLING_EDGE, cbf_hi)
    cb26 = pi.callback(p3, pigpio.FALLING_EDGE, cbf_26)

def execute(pi, p1, p2, p3, p4, o1):

    # pi = pigpio.pi() 

    pi.set_mode(lo, pigpio.INPUT)
    pi.set_mode(hi, pigpio.INPUT)
    pi.set_mode(26, pigpio.INPUT)

    pi.set_mode(20, pigpio.INPUT) # Later use this to ground RC
    pi.set_mode(21, pigpio.OUTPUT) # This is the output thru 2.2k

    tref=[]
    tsig1=[]
    tsig2=[]
    loopsum=0

    cblo = pi.callback(lo, pigpio.FALLING_EDGE, cbf_lo)
    cbhi = pi.callback(hi, pigpio.FALLING_EDGE, cbf_hi)
    cb26 = pi.callback(26, pigpio.FALLING_EDGE, cbf_26)
    
    gbl = globals()

    for i in range(samples):
        # Charge up RC Capacitor
        #print("P21 = 3.3V")
        pi.set_mode(o1, pigpio.OUTPUT)
        pi.write(o1, 1) # is this right? @dr smith
        
        time.sleep(0.05)
        
        # Prepare to disconnect P21
        gbl['tlo'] = 0
        gbl['thi'] = 0
        gbl['t26'] = 0
        #print("P21 = Input = Hi-Z")
        
        # Disconnect P21
        pi.set_mode(21, pigpio.INPUT)
        gbl['t0']  = pi.get_current_tick() # Get timestamp
        # While
        #  Any GPIO still is HI
        #   and
        #  Not timed out yet
        loops = 0
        while( ((gbl['tlo']==0) or (gbl['thi']==0) or (gbl['t26']==0)) and ((pi.get_current_tick()-t0) < 1000000)):
            time.sleep(0.01)
            loops +=1            # Count loops     
        # print(globals()['tlo'])
        #print("GPIO transition test loops=", loops)
        #print("Sample=", i, " tlo=", tlo, " thi=", thi, " t26=", t26)
        tref.append(gbl['tlo']  * 1e6) # low
        tsig1.append((gbl['thi'] - gbl['tlo'] ) * 1e6) # high
        tsig2.append((gbl['t26'] - gbl['tlo'] ) * 1e6) # us
        loopsum += loops
        
    gbl['tlo'] = 0
    gbl['thi'] = 0      
    gbl['t26'] = 0
    # Estimate RC and Vsig2
    RC = -1 * mean(tsig1)/math.log(Vreflo/Vrefhi)
    Vsig2 = Vrefhi*math.exp(-1 * mean(tsig2)/RC)
    return Vsig2