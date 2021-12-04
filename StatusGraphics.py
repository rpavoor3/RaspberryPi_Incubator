from tkinter import *
class StatusGraphics:
  root        = None
  alarm_state = True
  status      = None
  color       = None
  width       = None
  initialx    = None
  initialy    = None
  height_diff = None
  width_diff  = None
  height      = None
  bg          = None
  margin      = None

  def __init__(self, masterScreen, screen_width, screen_height, margin, machine_state, color='purple', bg='black'):
    self.color = color
    self.bg    = bg
    self.width = screen_width
    self.height = screen_height
    self.machine_state = machine_state
    self.margin = margin

    self.root = LabelFrame( masterScreen,                        # init master frame
                            text=' Status',
                            bd=0, font=('fixed', 32),
                            bg='black', fg=self.color,
                            labelanchor = 'n',
                            highlightbackground='dark cyan',
                            highlightcolor='dark slate grey',
                            highlightthickness=14,
                            padx=0, pady=0
                          )
    self.root.pack()                                      # pack and place on screen
    margin = self.margin
    self.initialx = self.width/2 + 1
    self.initialy = margin*self.height
    self.height_diff = self.height - self.initialy - margin*self.height
    self.width_diff = self.width/2 - margin*self.width


    self.root.place(x=self.initialx, y=self.initialy, height=self.height - self.initialy - margin*self.height, width= self.width/2 - margin*self.width)


    # init frame labels
    self.status = LabelFrame( self.root, 
                                padx=0, pady=0,bd=0
                              )
    self.status.pack()

    self.stateL = Label(self.root,
                            text='Status:',
                            fg=self.color,
                            bd=0, bg=self.bg,
                            anchor = 'center',
                            font=('fixed',  int(0.042*self.height), 'bold'),
                            padx=0, pady=0
                            )
    self.heating =    Label(self.root,
                          font=('fixed',  int(0.04*self.height)))
    self.heatingL = Label(self.root,
                            text='Heating:',
                            fg=self.color,
                            bd=0, bg=self.bg,
                            font=('fixed', int(0.042*self.height), 'bold'),
                            padx=0, pady=0
                            )
    self.alarm =    Label(self.root,
                          font=('fixed',  int(0.04*self.height)))

    self.alarmL = Label(self.root,
                            text='Alarm:',
                            fg=self.color,
                            bd=0, bg=self.bg,
                            font=('fixed', int(0.042*self.height), 'bold'),
                            padx=0, pady=20
                            )
    self.snooze =  Label(self.root, font=('fixed', int(0.04*self.height)))
    
    


    # pack and place on screen
    self.stateL.pack()
    self.stateL.place(x=0.35*self.width_diff, y=0.08*self.height_diff)
    self.heating.pack()
    self.heating.place(x=0.05*self.width_diff, y=0.28*self.height_diff)
    self.heatingL.pack()
    self.heatingL.place(x=0.35*self.width_diff, y=0.28*self.height_diff)
    self.alarm.pack()
    self.alarm.place(x=0.05*self.width_diff, y=0.48*self.height_diff)
    self.alarmL.pack()
    self.alarmL.place(x=0.35*self.width_diff, y =0.45*self.height_diff)
    self.snooze.pack()
    self.snooze.place(x=0.06*self.width_diff, y=0.53*self.height_diff)


    


    self.machine_state = machine_state
    


  def update(self):                    # init all sensor readings at each clock tick
    if any(self.machine_state.alarmCodes.values()):
        atext = ""
        color = 'red'
        for k,v in self.machine_state.alarmCodes.items():
            if v:
                atext = atext + str(k) +  '\n'
    else:
        color = 'green'
        atext = "ALL OKAY!"

    
    self.alarm.config( text='Alarm:',
        fg=self.color,
        bg=self.bg
        )
    
        
    self.alarmL.config( text=atext,
        fg=color,
        bg=self.bg
        )

    #Determining the state:
    (stateText, stateColor) = ('PREHEAT', 'dark yellow') if self.machine_state.is_preheating else ('ERROR', 'red') if self.machine_state.is_errored else ('RUNNING', 'green')

    self.stateL.config(text=stateText,
                        fg=stateColor,
                        bg=self.bg
                    )

    self.heating.config(text='Heating:',
                        fg=self.color,
                        bg=self.bg
                    )
    self.heatingL.config( text='ON' if self.machine_state.heaterOn else 'OFF',
        fg=self.color,
        bg=self.bg
        )
    
    if self.machine_state.is_snoozed:
        #symbol = '🔔'
        symbol = 'SNZ'
        time_remain = int(self.machine_state.snooze_countdown)  
        self.snooze.config(text=f'{symbol}\n{ str(int(time_remain/60))}:{ str(time_remain%60).zfill(2) }',
                        fg='yellow',
                        bg=self.bg
                    )     
    else:
        self.snooze.config(text='',
                        fg='yellow',
                        bg=self.bg
                    )


    #TODO: Add time left for snooze


    
    # update the warnings in newSensors.py for these values and then ,odify this part
    


    


    
