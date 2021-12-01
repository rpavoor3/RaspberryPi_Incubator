from tkinter import *
from PIL import Image, ImageTk
import time
from fillervals import TEMP,SPOINT

class PatientGraphics:
    root = None
    stats = None
    temp = None
    setpoint = None
    color = None
    tLabel = None
    spLabel = None
    bg = None
    machine_state = None

    def __init__(self, masterScreen, machine_state, color='green', bg='black'):
        self.color = color
        self.bg = bg

        self.root = LabelFrame(masterScreen,  # init master frame
                               text='  Patient',
                               bd=0, font=('fixed', 32),
                               bg=self.bg, fg=self.color,
                               highlightbackground='dark slate grey',
                               highlightcolor='dark slate grey',
                               highlightthickness=8,
                               padx=10, pady=0
                               )

        self.root.pack()  # pack and place on screen
        self.root.place(x=16, y=20, height=220, width=375)
        self.stats = LabelFrame(self.root,  # init stats frame
                                bd=0, bg=self.bg,
                                padx=10, pady=0
                                )

        self.stats.pack()  # pack and place on screen
        self.stats.place(x=140, y=0, height=150, width=150)

        # init frame labels
        self.temp = Label(self.stats, font=('fixed', 24))
        self.setpoint  = Label(self.stats, font=('fixed', 24))

        # pack and place on screen
        self.temp.pack()
        self.setpoint.pack()
        self.tLabel = Label(self.root,
                            text='Temperature:',
                            fg=self.color,
                            bd=0, bg=self.bg,
                            font=('fixed', 14),
                            padx=0, pady=0
                            )
        # set point
        self.spLabel = Label( self.root,
                          text='Desired Temp:', 
                          fg=self.color,
                          bd=0, bg=self.bg,
                          font=('fixed', 14),
                          padx=0, pady=0
                        )
        self.tLabel.pack()
        self.tLabel.place(x=20, y=0)
        self.spLabel.pack()
        self.spLabel.place(x=20, y=55)
        self.machine_state = machine_state
        


    def update(self):
        #temp = self.machine_state.skin_temp_reading
        #spoint = self.machine_state.set_point_reading
        temp = TEMP
        spoint = SPOINT

        self.temp.config(text='{0:.01f} °C'.format(float(temp)),
                         fg=self.color,
                         bg=self.bg
                         )
        self.setpoint.config(text='{0:.01f} °C'.format(float(spoint)),
                         fg=self.color,
                         bg=self.bg
            )

