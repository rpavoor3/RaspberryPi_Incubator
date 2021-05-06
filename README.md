# RasPi VitalsMonitor
Please go to the link below and follow the instructions to flash a SD card with the latest version of the Raspberry Pi OS with Desktop. 
Its best to use an SD card with storage > 8GB

https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up
## Current packages and pip modules needed on pi
* apt packages ("sudo apt-get install ..."):
  * python3
  * python3-tk
  * wmctrl
  * pigpio

* pip modules:
  * PIL
  * pytz
  * w1thermsensor

*Also included is a requirements.txt which will install all modules as well as the specifc version used to run this GUI*


# Configuring Pi

- In the raspberry pi configurations, 
on the interfaces tab, "serial port" and "1-wire" should both be enabled. 
## Ambient Temp
- The w1thermsensor is the python module for the ambient temperature sensor.
By default the pin is set to GPIO 4,however this differs from the pin on the PCB.
To change the gpio pin for the ambient temperature sensor do the following in terminal:
1. Type "sudo nano /boot/config.txt"
2. Scroll until "dtoverlay=w1-gpio,gpiopin=4" is shown.
3. Change "gpiopin=4" to "gpiopin=20" **NOTE: GPIO pin and Pi Pin on PCB are completely different**
4. Save changes and close file 
5. Reboot Pi.
## Start-Up
To help with auto-running the GUI do the follwing once terminal is open on the pi:
1. Type "sudo nano /etc/rc.local" to edit the local file.
2. Scroll all the way to the bottom of the file. Right before the "exit 0" and after "fi" type "sudo pigpiod". Save changes and close file.
3. Back on the terminal type "sudo nano /etc/xdg/autostart/display.desktop"
4. In the file edit,then copy and paste the following:
[Desktop Entry]
Name=RaspPi_VitalsMonitor
Exec=/usr/bin/python3 /home/pi/RaspPi_VitalsMonitor/Incubator.py 
5. Save changes and close file
6. Reboot your Pi and the Incubator GUI display will pop up.
**NOTE:** The GUI starts off waiting for input from the skin temp sensor. If not set up it will never turn on.

# Future Works
