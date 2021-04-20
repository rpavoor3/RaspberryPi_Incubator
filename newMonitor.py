from tkinter import *
from newPatient import infant
import newSensors
from newMachine import incubator
from pytz import timezone
from newAmbient import environment
import glob, time, datetime
from MonitorSettings import BG_COLOR,FONT_COLOR,TIMEZONE
class Monitor:
  root           = None
  clock          = None
  patientSensors = None
  ambientSensors = None
  status         = None
  patientStats   = None
  ambientStats   = None
  machineStats   = None
  normalColor    = FONT_COLOR
  bgColor        = BG_COLOR
  tz             = TIMEZONE
  currentTime    = None
  prevTime       = None

  def __init__(self):
    self.init_root()
    self.init_sensors()
    self.init_compartments()
    self.init_clock()
  
  def init_root(self):
    self.root = Tk()
    self.root.title('Incubator')
    self.root.configure(bg='black')
    self.root.geometry('800x480')

  def init_sensors(self):
    self.patientSensors = newSensors.Patient()
    self.ambientSensors = newSensors.Environment()
    self.status         = newSensors.MachineStatus(self.patientSensors, self.ambientSensors)

  def init_compartments(self):
    # if statments to block out stuff
    self.patientStats = infant(
                                self.root, self.patientSensors,
                                self.normalColor, self.bgColor
                              )
    self.machineStats = incubator(
                                    self.root, self.status,
                                    self.normalColor, self.bgColor
                                 )
    self.ambientStats = environment(
                                     self.root, self.ambientSensors,
                                     self.normalColor, self.bgColor
                                   )

  def init_clock(self):
    self.clock = Label(self.root, font=('fixed', 12))
    self.clock.place(x=431, y=8)              # Clock's Relative Position on Monitor
    
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
      
      self.clock.config( text= 'Date: ' + self.currentTime.strftime('%d-%b-%Y %I:%M %p') + str('        Power: {}'.format(self.AC_power_state())), 
                         fg='white',
                         bg=self.bgColor
                       )
    self.patientStats.update()
    self.machineStats.update()
    self.ambientStats.update()
    
    self.clock.after(50, self.update)

if __name__=='__main__':
  vm = Monitor()
  vm.update()
  vm.root.mainloop()

