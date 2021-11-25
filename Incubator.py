from tkinter import *
from ControlGraphics import infant
import Sensors
from EnvironmentGraphics import environment
from pytz import timezone
from StatusGraphics import incubator
import datetime
from config import BG_COLOR,FONT_COLOR,TIMEZONE
from fillervals import UUID

# TODO: ADD HEATING ELEMENT CODE AND OBJECT
'''
Monitor Class
Description: Primary driver of incubator software. Initializes each component, updates timer, and calls routines. 
'''
class Monitor:
  root           = None   # Tkinter Main Window
  banner  = None   # banner on top right
  environmentStats   = None   # Graphics for Probe and Ambient temperature
  controlStats   = None   # Graphic for Control compartment on the top
  statusStats   = None   # Graphic for the Status compartment
  normalColor    = FONT_COLOR
  bgColor        = BG_COLOR
  tz             = TIMEZONE
  currentTime    = None   # Calculate time for updating

  def __init__(self):
    # Initializing TKinter Window
    self.root = Tk()
    self.root.title('Incubator')
    self.root.configure(bg='black')
    self.root.geometry('800x480')

    # Initialize actual sensors
    self.init_sensors()

    # Inititalize remaining graphics
    self.init_compartments()
    self.init_clock_graphic()
    
    
    
  
  def init_sensors(self):
    #TODO: Init whateveer class will be reading the class and sending feedback (the class should update itself)    
    self.machine_state = Sensors.MachineStatus()
    

  def init_compartments(self):
    # For each stats object, intialize their graphics and attach their hardware components
    self.controlStats = infant(
                                self.root, self.machine_state,
                                self.normalColor, self.bgColor
                              )
    self.statusStats = incubator(
                                    self.root, self.machine_state, self.normalColor, self.bgColor
                                 )
    self.environmentStats = environment(
                                     self.root, self.machine_state,
                                     self.normalColor, self.bgColor
                                   )

    '''
    Display time and date
    '''
  def init_clock_graphic(self):
    self.banner= Label(self.root, font=('fixed', 12))
    self.banner.place(x=570, y=8)  # Clock's Relative Position on Monitor

  '''
  TODO: Rename clock graphic to banner. Add UUID/mac address/save a config to banner to reflect unique incubator.
  '''
  def update(self):
    # Get current time
    self.currentTime = datetime.datetime.now(timezone(self.tz))
    
    # Display clock graphic and power status (TODO along with UUID)
    self.banner.config( text= '\tUUID:' + str(UUID) + '\nDate: ' + self.currentTime.strftime('%d-%b-%Y %I:%M %p' ),
                         fg='white',
                         bg=self.bgColor
                       )

    # Read sensors and update graphics each heartbeat
    self.machine_state.update() #This updates the sensor readings (do we want this here?)
    self.environmentStats.update()
    self.controlStats.update()
    self.statusStats.update()
    
    # TODO: Replace clock graphic here with root and test
    # Bind update function to TK object, call every 50 ms
    # TODO: Get heartbeat from config
    self.banner.after(50, self.update)

if __name__=='__main__':
  vm = Monitor()
  vm.update()
  vm.root.mainloop()

