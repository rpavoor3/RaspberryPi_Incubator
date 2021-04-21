from tkinter import *
from PIL import Image, ImageTk
import time
import pigpio

blue = 22
orange = 17
green = 27

class infant:
    root = None
    hdr_font = None
    body_font = None
    stats = None
    bpm = None
    temp = None
    setpoint = None
    o2sat = None
    weight = None
    heart_rate = None
    color = None
    tLabel = None
    o2Label = None
    spLabel = None
    wLabel = None
    bg = None
    machine_state = None
    pi3     = pigpio.pi()

    def __init__(self, masterScreen, machine_state, color='blue', bg='black', hdr_font=32,body_font=14):
        self.hdr_font = hdr_font
        self.body_font = body_font
        self.color = color
        self.bg = bg

        self.root = LabelFrame(masterScreen,  # init master frame
                               text='  Patient',
                               bd=0, font=('fixed', 32),
                               bg=self.bg, fg=self.color,
                               highlightbackground='dark slate grey',
                               highlightcolor='dark slate grey',
                               highlightthickness=8,
                               padx=0, pady=0
                               )

        self.root.pack()  # pack and place on screen
        self.root.place(x=16, y=20, height=220, width=768)

        self.stats = LabelFrame(self.root,  # init stats frame
                                bd=0, bg=self.bg,
                                padx=10, pady=0
                                )

        self.stats.pack()  # pack and place on screen
        self.stats.place(x=64, y=0, height=150, width=325)

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
        
           # 17 is Orange LED 22-blue, 5-r
        self.pi3.set_mode(orange, pigpio.OUTPUT)
        self.pi3.write(orange, False)
        # 27 - green
        self.pi3.set_mode(green, pigpio.OUTPUT)
        self.pi3.write(green, False)
        # 22 - blue
        self.pi3.set_mode(blue, pigpio.OUTPUT)
        self.pi3.write(blue, False) 


    def update(self):

         temp = self.machine_state.skin_temp_reading
         spoint = self.machine_state.set_point_reading

        self.temp.config(text='{0:.01f} °C'.format(temp),
                         fg=self.color,
                         bg=self.bg
                         )
        self.setpoint.config(text='{0:.01f} °C'.format(spoint),
                         fg=self.color,
                         bg=self.bg
            )
        # temperature is just right - green
        if temp == spoint:
           self.pi3.write(green, True)
        else:
           self.pi3.write(green, False)
        # temperaure is too warm - orange
        if temp > spoint:
           self.pi3.write(orange, True)
        else:
           self.pi3.write(orange, False)
        # temperature is too cool - blue
        if temp < spoint:
            self.pi3.write(blue, True)
        else:
           self.pi3.write(blue, False)
           

