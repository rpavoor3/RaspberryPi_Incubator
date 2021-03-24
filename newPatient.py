from tkinter import *
from PIL import Image, ImageTk


class infant:
    root = None
    hdr_font = None
    body_font = None
    stats = None
    bpm = None
    temp = None
    o2sat = None
    weight = None
    heart_rate = None
    color = None
    tLabel = None
    o2Label = None
    wLabel = None
    bg = None
    sensors = None

    def __init__(self, masterScreen, sensors, color='blue', bg='black', hdr_font=32,body_font=14):
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

        # pack and place on screen
        self.temp.pack()
        self.tLabel = Label(self.root,
                            text='Temperature:',
                            fg=self.color,
                            bd=0, bg=self.bg,
                            font=('fixed', 14),
                            padx=0, pady=0
                            )
        self.tLabel.pack()
        self.tLabel.place(x=20, y=0)
        self.sensors = sensors

    def update(self):
        self.temp.config(text='{0:.01f} °C'.format(self.sensors.temperature()),
                         fg=self.color,
                         bg=self.bg
                         )

