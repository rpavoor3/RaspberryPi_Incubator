from tkinter import *
from newPatient import infant
import newSensors
from newMachine import incubator
from pytz import timezone
from newAmbient import environment
import glob, time, datetime
from MonitorSettings import BG_COLOR,FONT_COLOR,TIMEZONE

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
  prevTime       = None

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
    self.patientSensors = newSensors.Patient()
    self.ambientSensors = newSensors.Environment()

    # Pass in references to Patient and Ambient Sensors to alarm
    self.alarm_status   = newSensors.MachineStatus(self.patientSensors, self.ambientSensors)

  def init_compartments(self):
    # if statments to block out stuff
    self.patientStats = infant(
                                self.root, self.patientSensors,
                                self.normalColor, self.bgColor
                              )
    self.machineStats = incubator(
                                    self.root, self.alarm_status, self.normalColor, self.bgColor
                                 )
    self.ambientStats = environment(
                                     self.root, self.ambientSensors,
                                     self.normalColor, self.bgColor
                                   )

  def init_clock_graphic(self):
    self.clock_graphic = Label(self.root, font=('fixed', 12))
    self.clock_graphic.place(x=431, y=8)              # Clock's Relative Position on Monitor
    
  def AC_power_state(self):
    connected = False
    # can use \U000023FB and switch color to determine if disconencted or not
    if connected:
      return ' '
    else:
      return ''
    
    
      
  def update(self):
    self.currentTime = datetime.datetime.now(timezone(self.tz))
    
    if self.currentTime != self.prevTime:
      self.prevTime = self.currentTime
      
      self.clock_graphic.config( text= 'Date: ' + self.currentTime.strftime('%d-%b-%Y %I:%M %p') + str('        Power: {}'.format(self.AC_power_state())), 
                         fg='white',
                         bg=self.bgColor
                       )
    self.patientStats.update()
    self.machineStats.update()
    self.ambientStats.update()
    
    self.clock_graphic.after(50, self.update)

if __name__=='__main__':
  vm = Monitor()
  vm.update()
  vm.root.mainloop()

