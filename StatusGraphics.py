from tkinter import *
from fillervals import STATUS, STATE, HEATING, SNOOZE
class incubator:
  root        = None
  alarm_state = True
  status      = None
  color       = None
  bg          = None

  def __init__(self, masterScreen, machine_state, color='purple', bg='black'):
    self.color = color
    self.bg    = bg

    self.root = LabelFrame( masterScreen,                        # init master frame
                            text=' Status',
                            bd=0, font=('fixed', 32),
                            bg='black', fg=self.color,
                            highlightbackground='dark slate grey',
                            highlightcolor='dark slate grey',
                            highlightthickness=8,
                            padx=0, pady=0
                          )
    self.root.pack()                                      # pack and place on screen
    self.root.place(x=408, y=65, height=397, width=376)


    # init frame labels
    self.status = LabelFrame( self.root, 
                                padx=0, pady=0,
                                bd=0, font=('fit', 16)
                              )
    self.status.pack()
    self.state = Label(self.root, font=('fixed', 16))
    self.stateL = Label(self.root,
                            text='Status:',
                            fg=self.color,
                            bd=0, bg=self.bg,
                            font=('fixed', 16),
                            padx=0, pady=0
                            )
    self.heating = Label(self.root,
                            text='Heating:',
                            fg=self.color,
                            bd=0, bg=self.bg,
                            font=('fixed', 16),
                            padx=0, pady=0
                            )
    self.alarm =    Label(self.root,
                          font=('fixed', 16))

    self.alarmL = Label(self.root,
                            text='Alarm:',
                            fg=self.color,
                            bd=0, bg=self.bg,
                            font=('fixed', 18),
                            padx=0, pady=20
                            )
    self.snooze =  Label(self.root, font=('fixed', 16))
    
    


    # pack and place on screen
    self.stateL.pack()
    self.stateL.place(x=20, y=10)
    self.heating.pack()
    self.heating.place(x=20, y=75)
    self.alarm.pack()
    self.alarm.place(x=20, y=150 )
    self.alarmL.pack()
    self.alarmL.place(x=135, y = 137)
    self.snooze.pack()
    self.snooze.place(x=35, y= 173)

    


    self.machine_state = machine_state
    


  def update(self):                    # init all sensor readings at each clock tick
    
    atext = ""
    for a in STATUS:
        atext = atext + a +'\n'
    if len(STATUS) == 1:
        color = 'green'
    else:
        color = 'red'
    
    self.alarm.config( text='Alarm:',
        fg=self.color,
        bg=self.bg
        )
    
        
    self.alarmL.config( text=atext,
        fg=color,
        bg=self.bg
        )

    self.stateL.config(text='Status:         {}'.format(STATE),
                        fg=self.color,
                        bg=self.bg
                    )

    self.heating.config(text='Heating:        {}'.format(HEATING),
                        fg=self.color,
                        bg=self.bg
                    )

    if SNOOZE:
        symbol = '🔔'
    else:
        symbol = ' '
    self.snooze.config(text=symbol,
                        fg='yellow',
                        bg=self.bg
                    )
    #TODO: Add time left for snooze


    
    # update the warnings in newSensors.py for these values and then ,odify this part
    

    



    


    
