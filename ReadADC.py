from config import *
import pigpio
import time
import random
from statistics import pstdev
from statistics import mean
import math
import matplotlib.pyplot as plt

t0 = 0
t_lo = 0
t_hi = 0
t_read = 0

READ_PIN_ADC = PIN_BABY_TEMP

def cbf_lo(event, level, tick):
    #print("Tick from lo", tick)
    if (globals()['t_lo'] == 0):
        globals()['t_lo']  = tick - globals()['t0'] 

def cbf_hi(event, level, tick):
    # print("Tick from hi", tick)
    if (globals()['t_hi']  == 0):
        globals()['t_hi']  = tick - globals()['t0'] 
        
def cbf_read_baby(event, level, tick):
    # print("Tick from baby", tick)
    if (globals()['t_read']  == 0):
        globals()['t_read']  = tick - globals()['t0'] 

def main():
    # Constants
    Vrefhi = 12338/10000  # Volts
    Vreflo =  6168/10000  # Volts
    Vcc    = 33088/10000  # Volts
    samples = 50        # Samples for statistical estimate

    pi = pigpio.pi() 

    pi.set_mode(PIN_REF_LO, pigpio.INPUT)
    pi.set_mode(PIN_REF_HI, pigpio.INPUT)
    pi.set_mode(READ_PIN_ADC, pigpio.INPUT)

    # pi.set_mode(20, pigpio.INPUT) # Later use this to ground RC
    pi.set_mode(PIN_ADC_SOURCE, pigpio.OUTPUT) # This is the output thru 2.2k

    tref=[]
    tsig1=[]
    tsig2=[]
    loopsum=0

    cblo = pi.callback(PIN_REF_LO, pigpio.FALLING_EDGE, cbf_lo)
    cbhi = pi.callback(PIN_REF_HI, pigpio.FALLING_EDGE, cbf_hi)
    cbread = pi.callback(READ_PIN_ADC, pigpio.FALLING_EDGE, cbf_read_baby)
    
    gbl = globals()

    for i in range(samples):
        # Charge up RC Capacitor
        pi.set_mode(PIN_ADC_SOURCE, pigpio.OUTPUT)
        pi.write(PIN_ADC_SOURCE, 1)
        
        time.sleep(0.1)
        
        # Prepare to disconnect P21
        gbl['t_lo'] = 0
        gbl['t_hi'] = 0
        gbl['t_read'] = 0
        
        # Disconnect P21
        pi.set_mode(PIN_ADC_SOURCE, pigpio.INPUT) # ADC SOURCE PIN
        gbl['t0']  = pi.get_current_tick() # Get timestamp

        loops = 0
        while( ((gbl['t_lo']==0) or (gbl['t_hi']==0) or (gbl['t_read']==0)) and ((pi.get_current_tick()-t0) < 1 * 1e6)):
            time.sleep(0.01)
            loops +=1            # Count loops     

        print("Sample=", i, " t_lo=", t_lo, " t_hi=", t_hi, " t_read=", t_read)
        tref.append(gbl['t_hi']  * 1e6)
        tsig1.append((gbl['t_lo'] - gbl['t_hi'] ) * 1e6)
        tsig2.append((gbl['t_read'] - gbl['t_hi'] ) * 1e6)
        loopsum += loops
      
    # Remove outliers from tsig1 and tsig2
    tsig1_mean = mean(tsig1)
    tsig1_std = pstdev(tsig1)
    tsig1_upper = tsig1_mean + 2*tsig1_std
    tsig1_lower = tsig1_mean - 2*tsig1_std

    # Remove from tsig1
    tsig1_filtered = []
    for i in range(len(tsig1)):
        cur_val = tsig1[i]
        if (cur_val < tsig1_upper) and (cur_val > tsig1_lower):
            tsig1_filtered.append(cur_val)


    tsig2_mean = mean(tsig2)
    tsig2_std = pstdev(tsig2)
    tsig2_upper = tsig2_mean + 2*tsig2_std
    tsig2_lower = tsig2_mean - 2*tsig2_std
    # Remove from tsig2
    tsig2_filtered = []
    for i in range(len(tsig2)):
        cur_val = tsig2[i]
        if (cur_val < tsig2_upper) and (cur_val > tsig2_lower):
            tsig2_filtered.append(cur_val)
    


    print("loops: mean=", loopsum/samples)
    print(" tref: mean=", mean(tref),  " stdev=", pstdev(tref) )
    print("tsig1: mean=", mean(tsig1), " stdev=", pstdev(tsig1))
    print("tsig2: mean=", mean(tsig2), " stdev=", pstdev(tsig2))

    # Estimate RC and Vsig2
    RC = -1 * mean(tsig1)/math.log(Vreflo/Vrefhi)
    Vsig2 = Vrefhi*math.exp(-1 * mean(tsig2)/RC)

    print("Calculated: Vsig2=", Vsig2, "Volts,    RC=", RC, "Seconds   from Vrefhi and Vreflo")
    print("Done")

    # Estimate RC and Vsig2
    RC = -1 * mean(tsig1_filtered)/math.log(Vreflo/Vrefhi)
    Vsig2 = Vrefhi*math.exp(-1 * mean(tsig2_filtered)/RC)

    print("Calculated: Vsig2=", Vsig2, "Volts,    RC=", RC, "Seconds   from Vrefhi and Vreflo")
    print("Done")

    Vsig2_alt = Vrefhi*((Vreflo/Vrefhi)**(mean(tsig2_filtered)/mean(tsig1_filtered)))
    print("Calculated: Vsig2=", Vsig2_alt, "Volts,    RC=", RC, "Seconds   from Vrefhi and Vreflo")
    print("Done")

    # plt.plot(range(samples), tref,  label="tref")
    plt.plot(range(samples), tsig1, label="tsig1")
    plt.plot(range(samples), tsig2, label="tsig2")
    plt.legend()
    plt.show()



if __name__ == "__main__":
    main()

    
# Estimate RC and Vsig2 from Vcc and Vrefhi
# Not sure this is quite right
# RC = -1 * mean(tref)/math.log(Vrefhi/Vcc)
# Vsig2 = Vcc*math.exp(-1 * (mean(tsig2)+mean(tref))/RC)
# 
# print("Calculated: Vsig2=", Vsig2, "Volts,    RC=", RC, "Seconds  from Vcc and Vrefhi")

