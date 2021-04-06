from tkinter import *
import pigpio
red = 5
class incubator:
  root        = None
  #ac_pwr      = None
  alarm_state = True
  warnings    = None
  color       = None
  bg          = None
  pi2         = pigpio.pi()

  def __init__(self, masterScreen, status, color='purple', bg='black'):
    self.color = color
    self.bg    = bg

    self.root = LabelFrame( masterScreen,                        # init master frame
                            text=' Status',
                            bd=0, font=('fixed', 32),
                            bg='black', fg=self.color,
                            highlightbackground='dark slate grey',
                            highlightcolor='dark slate grey',
                            highlightthickness=8,
                            padx=2.5, pady=2.5
                          )
    self.root.pack()                                      # pack and place on screen
    self.root.place(x=408, y=252, height=212, width=376)

    # init frame labels
    #self.ac_pwr  = Label(self.root, font=('fixed', 24))
    self.alarm_status = Label(self.root, font=('fixed', 24))
    self.warnings = LabelFrame( self.root, 
                                padx=10, pady=10,
                                bd=0, font=('fixed', 20)
                              )

    self.temp = Label(self.warnings, font=('unifont', 24))
    self.humidity = Label(self.warnings, font=('fixed', 24))
    self.apnea = Label(self.warnings, font=('fixed', 24))
    self.hr = Label(self.warnings, font=('fixed', 26))
    self.o2 =  Label(self.warnings, font=('fixed', 24))


    # pack and place on screen
    #self.ac_pwr.pack()
    self.warnings.pack(fill='x')

    self.temp.pack(side=LEFT)
    self.humidity.pack()
    self.humidity.place(relx=0.25, rely=0)
    self.apnea.pack()
    self.apnea.place(relx=0.45, rely=0)
    self.hr.pack()
    self.hr.place(relx=0.65, rely=0.025)
    self.o2.pack(side=RIGHT)

    self.status = status
    

    # 5 - red
    self.pi2.set_mode(red, pigpio.OUTPUT)
    self.pi2.write(red, False)

  def update(self):                    # init all sensor readings at each clock tick
    warnings = self.status.check_alarms()
    '''
    self.ac_pwr.config( text='Power: {}'.format(self.status.AC_power_state()),
                        fg=self.color,
                        bg=self.bg
                      )
    '''
    self.warnings.config( text='Alarm Status: {}'.format(self.status.textToDisplay),
                          fg=self.color,
                          bg=self.bg
                        )

    self.temp.config( text='\ud83d\ude4f',
                      fg=warnings[0],
                      bg=self.bg
                    )
    
    # update the warnings in newSensors.py for these values and then ,odify this part
    '''
    if(warnings[1] or (warnings[2] or warnings[3] or warnings[4] ):
        self.pi2.write(red, True)
    else :
        self.pi2.write(red, False)
    
    
    self.humidity.config( text='\U0001F4A7',
                          fg=warnings[1],
                          bg=self.bg
                        )
    
    self.apnea.config( text='A',
                       fg=warnings[2],
                       bg=self.bg
                     )

    self.hr.config( text='\U00002665',
                    fg=warnings[3],
                    bg=self.bg
                  )

    self.o2.config( text='O₂',
                    fg=warnings[4],
                    bg=self.bg
                  )
    '''
