from tkinter import *
from PIL import Image, ImageTk
from fillervals import TEMP,SPOINT, AMB_TEMP, PROBE_TEMP

class PatientGraphics:
    root     = None
    width    = None
    height   = None
    stats    = None
    temp     = None
    setpoint = None
    color    = None
    tLabel   = None
    spLabel  = None
    atemp    = None
    probe    = None
    atempL   = None
    probeL   = None
    initialx = None
    initialy = None
    height_diff = None
    width_diff  = None
    bg       = None
    machine_state = None
    margin   = None

    def __init__(self, masterScreen, screenwidth, screenheight, margin, machine_state,color, bg='black'):
        self.width = screenwidth
        self.height = screenheight
        self.margin = margin

        self.color = color
        self.bg = bg
        self.machine_state = machine_state
        

        self.root = LabelFrame(masterScreen,  # init master frame
                               text='  Patient',
                               bd=0, font=('fixed', 32),
                               bg=self.bg, fg=self.color,
                               labelanchor = 'n',
                               highlightbackground='dark cyan',
                               highlightcolor='dark slate grey',
                               highlightthickness=14,
                               padx=10, pady=0
                               )
        
        self.root.pack()  # pack and place on screen
        margin = self.margin  # distance from edge of screen (margin * screen width or screen height)
        self.initialx = margin*self.width
        self.initialy = margin*self.height
        self.height_diff = self.height - margin * self.height - self.initialy
        self.width_diff = self.width/2 - self.initialx - 35
        self.root.place(x=self.initialx, y=self.initialy, height=(self.height - self.initialy) - margin * self.height, width=self.width/2 - self.initialx - 35)
        self.stats = LabelFrame(self.root,  # init stats frame
                                bd=0, bg=self.bg, fg=self.color,
                               highlightbackground='cyan',
                               highlightthickness=6,
                               padx=10, pady=0
                                )

        self.stats.pack()  # pack and place on screen
        self.stats.place(x=0.07*self.width_diff, y=0.05*self.height_diff, height=0.40*self.height_diff, width=0.75*self.width_diff)

        # init frame labels
        self.temp = Label(self.root, font=('fixed', int(0.13*self.height_diff)))
        self.setpoint  = Label(self.root, font=('fixed', int(0.03*self.height_diff)))
        self.atemp = Label(self.root, font=('fixed', int(0.045*self.height_diff)))
        self.probe   = Label(self.root, font=('fixed', int(0.045*self.height_diff)))
        self.sensor_count = Label(self.root, font=('fixed', int(0.09*self.height_diff)))

        # pack and place on screen
        self.temp.pack()
        self.setpoint.pack()

        self.tLabel = Label(self.root,
                            text='Control Temp:',
                            fg=self.color,
                            bd=0, bg=self.bg,
                            font=('fixed', int(0.03*self.height_diff)),
                            padx=0, pady=0
                            )
        # set point
        self.spLabel = Label( self.root,
                          text='Desired Temp:', 
                          fg=self.color,
                          bd=0, bg=self.bg,
                          font=('fixed', int(0.026*self.height_diff)),
                          padx=0, pady=0
                        )
        self.atempL = Label( self.root,
                         text='Ambient Temp:', 
                         fg=self.color,
                         bd=0, bg=self.bg,
                         font=('fixed', int(0.03*self.height_diff)),
                         padx=0, pady=0
                       )
    
        self.probeL = Label( self.root,
                          text='Monitoring Temp:', 
                          fg=self.color,
                          bd=0, bg=self.bg,
                          font=('fixed', int(0.03*self.height_diff)),
                          padx=0, pady=0
                        )
        
        
        self.temp.place(x=0.1*self.width_diff, y = 0.13*self.height_diff)
        self.setpoint.place(x=0.62*self.width_diff, y = 0.36*self.height_diff)
        self.tLabel.pack()
        self.tLabel.place(x=0.1*self.width_diff, y=0.07*self.height_diff)
        self.spLabel.pack()
        self.spLabel.place(x=0.32*self.width_diff, y=0.37*self.height_diff)

        self.atemp.pack()
        self.atemp.place(x=0.51*self.width_diff, y=0.55 *self.height_diff)
        self.probe.pack()
        self.probe.place(x=0.51*self.width_diff, y=0.73 *self.height_diff)

        self.atempL.pack()
        self.atempL.place(x=0.1*self.width_diff,y=0.55 *self.height_diff)
        self.sensor_count.pack()
        self.sensor_count.place(x=0.16*self.width_diff,  y=0.60*self.height_diff)
        self.probeL.pack()
        self.probeL.place(x=0.1*self.width_diff,y=0.73 *self.height_diff)
        


    def update(self):
        #temp = self.machine_state.skin_temp_reading
        #spoint = self.machine_state.set_point_reading

        self.temp.config(text='{0:.01f} °C'.format(float (self.machine_state.analogTempReading)),
                         fg='cyan',
                         bg=self.bg
                         )
        self.setpoint.config(text='{0:.01f} °C'.format(float (self.machine_state.setPointReading)),
                         fg=self.color,
                         bg=self.bg
            )
        atemp_val = float(sum(self.machine_state.ambientSensorReadings)/len(self.machine_state.ambientSensorReadings)) if len(self.machine_state.ambientSensorReadings) else 0
        self.atemp.config( text='{0:.01f} °C'.format(atemp_val),
                      fg=self.color,
                      bg=self.bg
                    )
    
                    
        self.probe.config( text='{0:.01f} °C'.format(float(self.machine_state.probeReading)),
                    fg=self.color,
                    bg=self.bg
                  )
        self.sensor_count.config( text='Sensor Count: {}'.format(len(self.machine_state.ambientSensorReadings)),
                    fg=self.color,
                    bg=self.bg
                  )
