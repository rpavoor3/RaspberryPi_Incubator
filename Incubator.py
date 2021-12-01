from tkinter import *
from ControlGraphics import PatientGraphics
from MachineState import MachineState
from Peripherals import PeripheralBus
from EnvironmentGraphics import AmbientGraphics
from pytz import timezone
from StatusGraphics import StatusGraphics
import datetime
from config import BG_COLOR,FONT_COLOR,TIMEZONE
from fillervals import UUID

# TODO: ADD HEATING ELEMENT CODE AND OBJECT
'''
Monitor Class
Description: Primary driver of incubator software. Initializes each component, updates timer, and calls routines. 
'''
class Incubator:
  rootWindow               = None   # Tkinter Main Window
  bannerGraphics             = None   # banner on top right
  ambientGraphics   = None   # Graphics for Probe and Ambient temperature
  patientGraphics       = None   # Graphic for Control compartment on the top
  statusGraphics        = None   # Graphic for the Status compartment
  normalColor        = FONT_COLOR
  bgColor            = BG_COLOR
  tz                 = TIMEZONE
  currentTime        = None   # Calculate time for updating
  machineState       = None
  peripheralBus      = None

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

    # Inititalize remaining graphics
    self.init_compartments()
    self.init_banner()
    

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

    '''
    Display time and date
    '''
  def init_banner(self):
    self.bannerGraphics= Label(self.rootWindow, font=('fixed', 12))
    self.bannerGraphics.place(x=570, y=8)  # Clock's Relative Position on Monitor

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
    # Manage state, manage alarm, snooze, etc

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

