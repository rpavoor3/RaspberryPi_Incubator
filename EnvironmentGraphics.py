from tkinter import *
from fillervals import AMB_TEMP, PROBE_TEMP

class environment:
  root    = None
  temp    = None
  tLabel  = None
  probe      = None
  probeLabel = None
  color   = None
  bg      = None
  machine_state = None
  
  '''
    NOTE: The humidity readings are all commmented out; once that gets
    implemented in the mySensors.py in the Environment classs, these can be
    uncommented to display the humidity
  '''

  def __init__(self, masterScreen, machine_state, color='green', bg='black'):
    self.color = color
    self.bg    = bg

    self.root = LabelFrame( masterScreen,                        # init master frame
                            text='  Environment',
                            bd=0, font=('fixed', 32),
                            bg=self.bg, fg=self.color,
                            highlightbackground='dark slate grey',
                            highlightcolor='dark slate grey',
                            highlightthickness=8,
                            padx=0, pady=0
                          )
    self.root.pack()                                      # pack and place on screen
    self.root.place(x=16, y=252, height=212, width=376)

    # init frame labels
    self.temp = Label(self.root, font=('fixed', 24))
    self.probe   = Label(self.root, font=('fixed', 24))

    self.tLabel = Label( self.root,
                         text='Ambient Temp:', 
                         fg=self.color,
                         bd=0, bg=self.bg,
                         font=('fixed', 14),
                         padx=0, pady=0
                       )
    
    self.probeLabel = Label( self.root,
                          text='Probe Temp:', 
                          fg=self.color,
                          bd=0, bg=self.bg,
                          font=('fixed', 14),
                          padx=0, pady=0
                        )
    

    # pack and place on screen
    self.temp.pack()
    self.temp.place(x=172, y=0)
    self.probe.pack()
    self.probe.place(x=172, y=45)

    self.tLabel.pack()
    self.tLabel.place(x=24,y=0)
    self.probeLabel.pack()
    self.probeLabel.place(x=24,y=45)

    self.machine_state = machine_state

  def update(self):
    self.temp.config( text='{0:.01f} °C'.format(AMB_TEMP),
                      fg=self.color,
                      bg=self.bg
                    )
    
                    
    self.probe.config( text='{0:.01f} °C'.format(PROBE_TEMP),
                    fg=self.color,
                    bg=self.bg
                  )
    