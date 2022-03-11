# RasPi VitalsMonitor
This code is intended to be used on a Raspberry Pi 3B+. 
Please go to the link below and follow the instructions to flash a SD card with the latest version of the Raspberry Pi OS with Desktop. 
Its best to use an SD card with storage > 8GB
https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up

## Step 1) Current packages and pip modules needed on pi
* apt packages ("sudo apt-get install ..."):
  * python3
  * python3-tk
  * wmctrl
  * pigpio
  * python3-gpiozero

* pip modules ("sudo pip install..."):
  * Pillow (may already be installed)
  * pytz

* the pigpiod daemon:
  * "sudo pigpiod"

## Step 2) Configuring Pi
- In the Raspberry Pi Configurations, 
on the interfaces tab, "serial port" and "1-wire" should be enabled.


## Step 3)Test execution
- With python3, run _Incubator.py_ (the main entry point for the program) 
  - Note: The Pi does not need to be connected to the Incubator for this program to run)
  - If 'PIL' is not found or 'ImageTk' is not found, try installing ImageTk manually ("sudo apt-get install python3-pil.imagetk") 
- You should not receive any errors, but please address them if you do. **Make sure that the program runs and you can see the GUI before continuing**



## Step 4) Start-Up Script
To help with auto-running the GUI do the follwing once terminal is open on the pi:
1. Type "sudo nano /etc/rc.local" to edit the local file.
2. Scroll all the way to the bottom of the file. Right before the "exit 0" and after "fi" type *sudo pigpiod*. 
3. Save changes and close file
4. Create an "autostart" directory in the ".config" directory ("mkdir /home/pi/.config/autostart")
5. Navigate to that directory using the command line, and type "nano inky.desktop")
6. In the file, add these these lines  
*[Desktop Entry]*  
*Type=Application*  
*Name=Inky*  
*Exec=/usr/bin/python3 /home/pi/RaspberryPi_Incubator/Incubator.py*  
7. Save changes and close file
8. Reboot pi
9. If the GUI does NOT start up automatically, read the **Troubleshooting Start-Up** section
10. Note: You are free to use any start-up script method that you'd like, but the "autostart" method described here is preferred.

## Troubleshooting Start-Up
1. If the Pi is not booting up(only a blank screen is showing up), give it some them and check to see if there is enough power going into the Pi.
  - If so, Try unplugging it, and plugging it in again ad waiting. 
  - If you only see a blank screen after many attempts(unlikely), it is possible that there was the script interferred with the bootup process and you may have to re-flash the microSD card and start over.
2. If the Pi does start up, we need to see the error that is occuring. To do this, we need to use **xterm**. Type "sudo apt-get install xterm -y" into command terminal.
  - In /home/pi/.config/autostart/ink.py, change the "Exec" line to:  
    Exec=xterm -hold -e 'usr/bin/python3 /home/pi/RaspberryPi_Incubator/Incubator.py  
  - Reboot Pi
  - The xterm terminal should show up, and you will be able to see the error. 
  - If you don't see the terminal after the Pi boots, the .desktop file may not be in the correct directory or there are spelling mistakes

* Look at this link for more debugging tips: https://learn.sparkfun.com/tutorials/how-to-run-a-raspberry-pi-program-on-startup/method-2-autostart



# TODO
* Some form of set up validation script (specifically for one wire)

## Ambient Temp OneWire
By default the pin is set to GPIO 4,however this differs from the pin on the PCB.
To change the gpio pin for the ambient temperature sensor do the following in terminal:
1. Type "sudo nano /boot/config.txt"
2. Scroll until "dtoverlay=w1-gpio,gpiopin=4" is shown.
3. Change "gpiopin=4" to "gpiopin=20"
4. Save changes and close file 
5. Reboot Pi.
NOTE: These pin numbers will likely change with PCB revision

# Future Works
* Implement more sensors to incubator
* Create method to collect data from multiple incubators
