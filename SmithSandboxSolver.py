#!/usr/bin/python
#
# Copyright Whit Smith 2022 February 15
# Solving for mystery voltages and time constant in RC circuit
#
#

# To install scipy on RPi
# 
# sudo apt update
# sudo apt install -y python3-scipy
# 
# from
# https://stackoverflow.com/questions/59994060/cant-install-scipy-to-raspberry-pi-4-raspbian


import time

# Colored text
# 
# https://pypi.org/project/colorama/
# Available formatting constants are:
#     Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
#     Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
#     Style: DIM, NORMAL, BRIGHT, RESET_ALL
#     
# Other colored text options https://www.studytonight.com/python-howtos/how-to-print-colored-text-in-python
# 
import colorama   # Colored text
from colorama import Fore, Style
#import math


#
# Test Example
#
tp = 0               # Time departing positive extreme
tdr = 1.1702 + tp    # Time decending through reference voltage
tdx = 1.0180 + tdr   # Time decending through mystery voltage
tux = 2.000          # Time ascending through mystery voltage
tur = 0.2526 + tux   # Time ascending through reference voltage
vr = 1.024           # Reference voltage

##vp = 3.3     # Voltage positive rail
##vr = 1.024   # Voltage reference
##vx = 0.370   # Voltage to be identified

from scipy.optimize import fsolve
from scipy.optimize import root
from math import exp
from math import floor


# Functions to be numerically minimized by fsolve() or root()
#
def func(x):
    vp = x[0]
    vx = x[1]
    RC = x[2]

    return([
        vp * exp(-((tdr-tp )/RC)) - vr,
        vr * exp(-((tdx-tdr)/RC)) - vx,
        (vp-vx)*(1 - exp(-(tur-tux)/RC)) + vx - vr
        ])


tstart = time.time()
loop = 100
for i in range(loop):
    root = fsolve(func, [1,1,1])   # [vp, vx, RC] Initial conditions
#root = fsolve(func, [3.0, 0.5, 2])
#root = fsolve(func, [3.0, 0.35, 0.5])
#root = root(func, [3.0, 0.35, 0.5])
tend = time.time()


# Play with Python terminal formatting
print('[vp, vx, RC] = ',root)
txt = 'vp = {rootx[0]:.3f} Volts, vx = {rootx[1]:.3f} Volts, RC = {rootx[2]:.3f} Seconds'
print(txt.format(rootx=root))

# Better answers on RPi vs Desktop PC: Probably better time() resolution
print('Tstart =' , tstart)
print('Tend   =' , tend)
print('Total solve time = ', (tend-floor(tend)) - (tstart-floor(tstart)) )
print(Fore.GREEN + '      Solve time = ', (tend-tstart)/loop )

# Reset printing styles
print(Style.RESET_ALL)
print("Done")

