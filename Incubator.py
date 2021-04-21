from tkinter import *
from PatientGraphics import infant
import Sensors
from MachineGraphics import incubator
from pytz import timezone
from AmbientGraphics import environment
import glob, time, datetime
from MonitorSettings import BG_COLOR,FONT_COLOR,TIMEZONE

# TODO: ADD HEATING ELEMENT CODE AND OBJECT

'''
Monitor Class
Description: Primary driver of incubator software. Initializes each component, updates timer, and calls routines. 
'''
class Monitor:
  root           = None   # Tkinter Main Window
  clock_graphic  = None   # Clock graphic on main
  patientSensors = None   # Patient sensors (HR, Skin Temp)
  ambientSensors = None   # Incubator sensors (Temp of incubator, humidity)
  alarm_status   = None   # Determine and set alarm status
  patientStats   = None   # Graphics for patient
  ambientStats   = None   # Graphic for ambient
  machineStats   = None   # Graphic for machine stats
  normalColor    = FONT_COLOR
  bgColor        = BG_COLOR
  tz             = TIMEZONE
  currentTime    = None   # Calculate time for updating
  machineState   = None

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
    self.machine_state = Sensors.MachineStatus()
    '''
    self.patientSensors = Sensors.Patient_Sensors()
    self.ambientSensors = Sensors.Ambient_Sensors()

    # Pass in references to Patient and Ambient Sensors to alarm
    self.alarm_status   = Sensors.MachineStatus(self.patientSensors, self.ambientSensors)
    '''

  def init_compartments(self):
    # For each stats object, intialize their graphics and attach their hardware components
    self.patientStats = infant(
                                self.root, self.machine_state,
                                self.normalColor, self.bgColor
                              )
    self.machineStats = incubator(
                                    self.root, self.machine_state, self.normalColor, self.bgColor
                                 )
    self.ambientStats = environment(
                                     self.root, self.machine_state,
                                     self.normalColor, self.bgColor
                                   )

'''
Display time and date
'''
  def init_clock_graphic(self):
    self.clock_graphic = Label(self.root, font=('fixed', 12))
    self.clock_graphic.place(x=431, y=8)  # Clock's Relative Position on Monitor

'''
TODO: Update code to reflect whether we are connected to wall or battery
'''    
  def AC_power_state(self):
    connected = False
    if connected:
      return ' '
    else:
      return ''
    
    
  '''
  TODO: Rename clock graphic to banner. Add UUID/mac address/save a config to banner to reflect unique incubator.
  '''
  def update(self):
    # Get current time
    self.currentTime = datetime.datetime.now(timezone(self.tz))
    
    # Display clock graphic and power status (TODO along with UUID)
    self.clock_graphic.config( text= 'Date: ' + self.currentTime.strftime('%d-%b-%Y %I:%M %p') \
       + str('        Power: {}'.format(self.AC_power_state())), 
                         fg='white',
                         bg=self.bgColor
                       )

    # Read sensors and update graphics each heartbeat
    self.machine_state.update()
    self.patientStats.update()
    self.machineStats.update()
    self.ambientStats.update()
    
    # TODO: Replace clock graphic here with root and test
    # Bind update function to TK object, call every 50 ms
    # TODO: Get heartbeat from config
    self.clock_graphic.after(50, self.update)

if __name__=='__main__':
  vm = Monitor()
  vm.update()
  vm.root.mainloop()

