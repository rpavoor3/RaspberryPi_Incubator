from tkinter import *

from gpiozero.output_devices import OutputDevice
from ControlGraphics import PatientGraphics
from MachineState import MachineState
from Peripherals import PeripheralBus
from EnvironmentGraphics import AmbientGraphics
from pytz import timezone
from StatusGraphics import StatusGraphics
import datetime
from config import *
from fillervals import UUID
from gpiozero import DigitalOutputDevice

# TODO: ADD HEATING ELEMENT CODE AND OBJECT
'''
Monitor Class
Description: Primary driver of incubator software. Initializes each component, updates timer, and calls routines. 
'''
class Incubator:
  
  # Graphics
  rootWindow               = None   # Tkinter Main Window
  bannerGraphics             = None   # banner on top right
  ambientGraphics   = None   # Graphics for Probe and Ambient temperature
  patientGraphics       = None   # Graphic for Control compartment on the top
  statusGraphics        = None   # Graphic for the Status compartment
  normalColor        = FONT_COLOR
  bgColor            = BG_COLOR
  tz                 = TIMEZONE
  currentTime        = None   # Calculate time for updating
  # State Management
  machineState       = None
  # Peripheral Subsystem
  peripheralBus      = None
  # Heating Control
  heaterDevice       = None

  def __init__(self):
    # Initializing TKinter Window
    self.rootWindow = Tk()
    self.rootWindow.title('Incubator')
    self.rootWindow.configure(bg='black')
    self.rootWindow.geometry('800x480')

    # Initialize state bus
    self.machineState = MachineState()

    # Initialize peripheral bus 
    self.peripheralBus = PeripheralBus(self.machineState)

    # Initialize heating system control device
    self.heaterDevice = DigitalOutputDevice(9)

    # Inititalize remaining graphics
    self.init_compartments()
    self.init_banner()
    
  def init_banner(self):
    self.bannerGraphics= Label(self.rootWindow, font=('fixed', 12))
    self.bannerGraphics.place(x=570, y=8)  # Clock's Relative Position on Monitor

  def init_compartments(self):
    # For each stats object, intialize their graphics and attach their hardware components
    self.patientGraphics = PatientGraphics(
                                self.rootWindow, self.machineState,
                                self.normalColor, self.bgColor
                              )
    self.statusGraphics = StatusGraphics(
                                    self.rootWindow, self.machineState, self.normalColor, self.bgColor
                                 )
    self.ambientGraphics = AmbientGraphics(
                                     self.rootWindow, self.machineState,
                                     self.normalColor, self.bgColor
                                   )

  def process(self):

    # Heating System Control
    if (self.machineState.heaterOn and
        self.machineState.analogTempReading > self.machineState.setPointReading + CONTROL_THRESHOLD):
        # Turn Heater Off
        self.machineState.heaterOn = False
        self.heaterDevice.off()

    elif (not self.machineState.heaterOn and
          self.machineState.analogTempReading < self.machineState.setPointReading - CONTROL_THRESHOLD):
          # Turn Heater on
          self.machineState.heaterOn = True
          self.heaterDevice.on()

    # Check for temperature out of alarm range
    if (self.machineState.analogTempReading > self.machineState.setPointReading + ALARM_THRESHOLD):
      self.machineState.alarmCodes["Too Hot"] = True
    else:
      self.machineState.alarmCodes["Too Hot"] = False

    if (self.machineState.analogTempReading < self.machineState.setPointReading - ALARM_THRESHOLD):
      self.machineState.alarmCodes["Too Cold"] = True
    else:
      self.machineState.alarmCodes["Too Cold"] = False

    # Check for heater malfunction
    if (self.machineState.physicalControlLine):
      self.machineState.alarmCodes["Heater Malfunction"] = (not all(self.machineState.heaterStates))
    else:
      self.machineState.alarmCodes["Heater Malfunction"] = any(self.machineState.heaterStates)

    # Check for major system errors
    if (self.machineState.alarmCodes["Control Sensor Malfunction"]):
      self.machineState.is_errored = True
    else:
      self.machineState.is_errored = False

    # Check if temperature shutdown (thermostat failsafe activated)
    self.machineState.alarmCodes["Temperature Shutdown"] = (self.machineState.physicalControlLine and not self.machineState.physicalHeaterCommand)

    # Check if alarm needs to sound
    self.machineState.soundAlarm = self.machineState.alarmCodes["Too Cold"] or self.machineState.alarmCodes["Too Hot"] 
    
    # Check for preheat state transition
    if self.machineState.is_preheating and self.machineState.analogTempReading >= self.machineState.setPointReading:
      self.machineState.is_preheating = False
 

  '''
  TODO: Rename clock graphic to banner. Add UUID/mac address/save a config to banner to reflect unique incubator.
  '''
  def update(self):
    # Get current time
    self.currentTime = datetime.datetime.now(timezone(self.tz))
    
    # Display clock graphic and power status (TODO along with UUID)
    self.bannerGraphics.config( text= '\tUUID:' + str(UUID) + '\nDate: ' + self.currentTime.strftime('%d-%b-%Y %I:%M %p' ),
                         fg='white',
                         bg=self.bgColor
                       )

    # Read sensors and update state
    self.peripheralBus.update()

    # Do control system post proccessing here
    self.process()

    # Update outputs
    self.peripheralBus.writeOutput()

    # Update graphics
    self.ambientGraphics.update()
    self.patientGraphics.update()
    self.statusGraphics.update()
 
    
    # TODO: Replace clock graphic here with root and test
    # Bind update function to TK object, call every 50 ms
    # TODO: Get heartbeat from config
    self.bannerGraphics.after(50, self.update)

if __name__=='__main__':
  incubator = Incubator()
  incubator.update()
  incubator.rootWindow.mainloop()

