# RasPi VitalsMonitor

## Current packages and pip modules needed on pi
* apt packages:
  * python3
  * python3-tk
  * wmctrl
  * pigpio

* pip modules:
  * PIL
  * pytz
  * w1thermsensor


onewire, script to auto run code, restart pi if more than one ambient temp sensor is added 

## Start-Up
To help with auto-running the GUI do the following on the command terminal of the pi:
1. Type "sudo nano /etc/rc.local" to edit the local file.
2. Scroll all the way to the bottom of the file. Right before the "exit 0" type "sudo pigpio." Close file and save changes.
3. Type "sudo crontab -e"
4. Once again scroll all the way to the bottom of the file. 
Type "@reboot python3 /{path-to-Raspi_VitalsMonitor}/Incubator.py &." Close file and save changes.
5. Reboot your Pi and the Incubator GUI display will pop up.