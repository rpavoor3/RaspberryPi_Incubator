import pigpio
import time
import random
import matplotlib.pyplot as plt
from statistics import pstdev
from statistics import mean
import math

t0 = 0
t12 = 0
t13 = 0
t26 = 0

def cbf_12(event, level, tick):
    # print("Tick from 12", tick)
    if (globals()['t12'] == 0):
        globals()['t12']  = tick - globals()['t0'] 

def cbf_13(event, level, tick):
    # print("Tick from 13", tick)
    if (globals()['t13']  == 0):
        globals()['t13']  = tick - globals()['t0'] 
        
def cbf_26(event, level, tick):
    # print("Tick from 26", tick)
    if (globals()['t26']  == 0):
        globals()['t26']  = tick - globals()['t0'] 

def main():
    # Constants
    Vrefhi = 1021/1000  # Volts
    Vreflo =  500/1000  # Volts
    Vcc    = 3297/1000  # Volts
    samples = 200        # Samples for statistical estimate

    pi = pigpio.pi() 

    pi.set_mode(12, pigpio.INPUT)
    pi.set_mode(13, pigpio.INPUT)
    pi.set_mode(26, pigpio.INPUT)

    pi.set_mode(20, pigpio.INPUT) # Later use this to ground RC
    pi.set_mode(21, pigpio.OUTPUT) # This is the output thru 2.2k

    tref=[]
    tsig1=[]
    tsig2=[]
    loopsum=0

    cb12 = pi.callback(12, pigpio.FALLING_EDGE, cbf_12)
    cb13 = pi.callback(13, pigpio.FALLING_EDGE, cbf_13)
    cb26 = pi.callback(26, pigpio.FALLING_EDGE, cbf_26)
    
    gbl = globals()

    for i in range(samples):
        # Charge up RC Capacitor
        #print("P21 = 3.3V")
        pi.set_mode(21, pigpio.OUTPUT)
        pi.write(21, 1) # is this right? @dr smith
        
        time.sleep(0.05)
        
        # Prepare to disconnect P21
        gbl['t12'] = 0
        gbl['t13'] = 0
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
        while( ((gbl['t12']==0) or (gbl['t13']==0) or (gbl['t26']==0)) and ((pi.get_current_tick()-t0) < 1000000)):
            time.sleep(0.01)
            loops +=1            # Count loops     
        # print(globals()['t12'])
        #print("GPIO transition test loops=", loops)
        #print("Sample=", i, " t12=", t12, " t13=", t13, " t26=", t26)
        tref.append(gbl['t12']  * 1e6)
        tsig1.append((gbl['t13'] - gbl['t12'] ) * 1e6)
        tsig2.append((gbl['t26'] - gbl['t12'] ) * 1e6)
        loopsum += loops
        

    print("loops: mean=", loopsum/samples)
    print(" tref: mean=", mean(tref),  " stdev=", pstdev(tref) )
    print("tsig1: mean=", mean(tsig1), " stdev=", pstdev(tsig1))
    print("tsig2: mean=", mean(tsig2), " stdev=", pstdev(tsig2))

    # Estimate RC and Vsig2 from Vcc and Vrefhi
    # Not sure this is quite right
    # RC = -1 * mean(tref)/math.log(Vrefhi/Vcc)
    # Vsig2 = Vcc*math.exp(-1 * (mean(tsig2)+mean(tref))/RC)
    # 
    # print("Calculated: Vsig2=", Vsig2, "Volts,    RC=", RC, "Seconds  from Vcc and Vrefhi")


    # Estimate RC and Vsig2
    RC = -1 * mean(tsig1)/math.log(Vreflo/Vrefhi)
    Vsig2 = Vrefhi*math.exp(-1 * mean(tsig2)/RC)

    print("Calculated: Vsig2=", Vsig2, "Volts,    RC=", RC, "Seconds   from Vrefhi and Vreflo")

    plt.plot(range(samples), tref,  label="tref")
    plt.plot(range(samples), tsig1, label="tsig1")
    plt.plot(range(samples), tsig2, label="tsig2")
    plt.legend()
    plt.show()

    print("Done")

if __name__ == "__main__":
    main()