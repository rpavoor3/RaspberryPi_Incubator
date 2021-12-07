from tkinter import *

from gpiozero.output_devices import OutputDevice
from ControlGraphics import PatientGraphics
from MachineState import MachineState
from Peripherals import PeripheralBus
from pytz import timezone
from StatusGraphics import StatusGraphics
import time
from config import *
from fillervals import UUID
from uuid import getnode as get_mac
from gpiozero import DigitalOutputDevice
from gpiozero.pins.pigpio import PiGPIOFactory

# TODO: ADD HEATING ELEMENT CODE AND OBJECT
'''
Monitor Class
Description: Primary driver of incubator software. Initializes each component, updates timer, and calls routines. 
'''
class Incubator:
  
  # Graphics
  rootWindow          = None   # Tkinter Main Window
  bannerGraphics      = None   # Banner on the top
  patientGraphics     = None   # Graphic for Control compartment on the top
  statusGraphics      = None   # Graphic for the Status compartment
  normalColor         = FONT_COLOR
  bgColor             = BG_COLOR
  tz                  = TIMEZONE
  startTime           = None   # Calculate time for updating
  # State Management
  machineState       = None
  # Peripheral Subsystem
  peripheralBus      = None
  # Heating Control
  heaterDevice       = None
  screen_width       = None
  screen_height      = None
  margin             = None  #window margins
  uuid               = None

  def __init__(self):
    # Initializing TKinter Window
    self.rootWindow = Tk()
    self.rootWindow.attributes('-fullscreen', True) 
    self.rootWindow.title('Incubator')
    self.rootWindow.configure(bg='black')
    self.screen_width = self.rootWindow.winfo_screenwidth()
    self.screen_height = self.rootWindow.winfo_screenheight()
    self.rootWindow.geometry(f'{self.screen_width}x{self.screen_height}')
    self.rootWindow.bind("<Escape>", self.end_fullscreen)
    self.margin = 0.05
    mac = get_mac()
    macString = ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))
    self.uuid = macString

    # Initialize state bus
    self.machineState = MachineState()

    self.rootWindow.bind("<Up>", self.incSP)
    self.rootWindow.bind("<Down>", self.decSP)

    # Initialize peripheral bus 
    self.peripheralBus = PeripheralBus(self.machineState)

    factory = PiGPIOFactory()
    # Initialize heating system control device
    self.heaterDevice = DigitalOutputDevice(21, pin_factory=factory, initial_value=True)

    # Inititalize remaining graphics
    self.init_compartments()
    self.init_banner()
    
  def init_banner(self):
    self.startTime = round(time.time())
    self.bannerGraphics= Label(self.rootWindow, bg= 'dark blue',font=('fixed', 14), anchor = 'e')
    self.bannerGraphics.place(x=self.margin * self.screen_width, y=0, width = self.screen_width - 2*self.margin * self.screen_width)  # Clock's Relative Position on Monitor

  def init_compartments(self):
    # For each stats object, intialize their graphics and attach their hardware components
    self.patientGraphics = PatientGraphics(
                                self.rootWindow,self.screen_width, self.screen_height, 
                                self.margin, self.machineState, self.normalColor, self.bgColor
                              )
    self.statusGraphics = StatusGraphics(
                                    self.rootWindow, self.screen_width, self.screen_height, 
                                    self.margin, self.machineState, self.normalColor, self.bgColor
                                 )
                                 
  def end_fullscreen(self, event=None):
    self.state = False
    self.rootWindow.attributes("-fullscreen", False)
    return

  def incSP(self, event=None):
    if self.machineState != None:
      self.machineState.setPointReading += 0.5
  
  def decSP(self, event=None):
    if self.machineState != None:
      self.machineState.setPointReading -= 0.5
      
  def process(self):
    # Heating System Control
    #TODO: look at transition state, the system will fail ON for some reason when you initialize
    if (self.machineState.heaterOn and
        self.machineState.probeReading > self.machineState.setPointReading + CONTROL_THRESHOLD):
        # Turn Heater Off
        self.machineState.heaterOn = False
        self.heaterDevice.on()

    elif (not self.machineState.heaterOn and
          self.machineState.probeReading < self.machineState.setPointReading - CONTROL_THRESHOLD):
          # Turn Heater on
          self.machineState.heaterOn = True
          self.heaterDevice.off()

    # Check for temperature out of alarm range
    if (self.machineState.probeReading > self.machineState.setPointReading + ALARM_THRESHOLD):
      self.machineState.alarmCodes["Too Hot"] = True
    else:
      self.machineState.alarmCodes["Too Hot"] = False

    if (self.machineState.probeReading < self.machineState.setPointReading - ALARM_THRESHOLD):
      self.machineState.alarmCodes["Too Cold"] = True
    else:
      self.machineState.alarmCodes["Too Cold"] = False

    # Check for heater malfunction
    if (self.machineState.physicalControlLine):
      self.machineState.alarmCodes["Heater Malfunction"] = (not all(self.machineState.heaterStates))
    else:
      self.machineState.alarmCodes["Heater Malfunction"] = any(self.machineState.heaterStates)


    # Check if temperature shutdown (thermostat failsafe activated)
    self.machineState.alarmCodes["Temperature Shutdown"] = (self.machineState.physicalControlLine and not self.machineState.physicalHeaterCommand)

    # Check for major system errors
    if (self.machineState.alarmCodes["Control Sensor Malfunction"]):
      self.machineState.is_errored = True
    else:
      self.machineState.is_errored = False

    # Check if alarm needs to sound
    self.machineState.soundAlarm = self.machineState.alarmCodes["Too Cold"] or self.machineState.alarmCodes["Too Hot"] or self.machineState.alarmCodes["Temperature Shutdown"] 
    
    # Check for preheat state transition
    if self.machineState.is_preheating and self.machineState.analogTempReading >= self.machineState.setPointReading:
      self.machineState.is_preheating = False
 

  '''
  TODO: Rename clock graphic to banner. Add UUID/mac address/save a config to banner to reflect unique incubator.
  '''
  def update(self):
    s = time.time()
    # Get current time
    currentTime = round(time.time()- self.startTime)
    hours = int(currentTime / 3600)
    mins = int((currentTime - (hours * 3600)) / 60)
    secs = int(currentTime % 60)
    
    # Display clock graphic and power status (TODO along with UUID)
    self.bannerGraphics.config( text= f"UUID: {str(self.uuid)}\tTime Elapsed: {hours}:{str(mins).zfill(2)}:{str(secs).zfill(2)}",
                           fg='white',
                           bg='dark slate blue'
                       )
    t = time.time()
    # Read sensors and update state
    self.peripheralBus.update()
    #print("Sensor Reading:", time.time() - t)
    t = time.time()

    # Do control system post proccessing here
    self.process()
    #print("Processing:", time.time() - t)
    t = time.time()

    # Update outputs
    self.peripheralBus.writeOutput()
    #print("Write output:", time.time() - t)
    t = time.time()

    # Update graphics
    self.patientGraphics.update()
    self.statusGraphics.update()
    #print("Graphics Update:", time.time() - t)

 
    
    # TODO: Replace clock graphic here with root and test
    # Bind update function to TK object, call every 50 ms
    # TODO: Get heartbeat from config
    self.bannerGraphics.after(50, self.update)
    #print("Total Execution:", time.time() - s)
    #print("\n-------------------------------\n")

if __name__=='__main__':
  incubator = Incubator()
  incubator.update()
  incubator.rootWindow.mainloop()

