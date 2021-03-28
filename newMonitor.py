from tkinter import *
from newPatient import infant
import newSensors
from pytz import timezone
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

  def init_compartments(self):
    # if statments to block out stuff
    self.patientStats = infant(
                                self.root, self.patientSensors,
                                self.normalColor, self.bgColor
                              )

  def init_clock(self):
    self.clock = Label(self.root, font=('fixed', 12))
    self.clock.place(x=616, y=8)              # Clock's Relative Position on Monitor
    
  def check_alarms(self):
      self.patientStats.alarmcheck()
      
      
  def update(self):
    self.currentTime = datetime.datetime.now(timezone(self.tz))
    
    if self.currentTime != self.prevTime:
      self.prevTime = self.currentTime
      
      self.clock.config( text=self.currentTime.strftime('%d-%b-%Y %I:%M %p'),
                         fg='white',
                         bg=self.bgColor
                       )
    self.patientStats.update()
    self.check_alarms()
    self.clock.after(100, self.update)

if __name__=='__main__':
  vm = Monitor()
  vm.update()
  vm.root.mainloop()

