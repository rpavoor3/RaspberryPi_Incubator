class MachineState:

    # Push button managed states
    is_snoozed = False
    is_snooze_requested = False
    is_preheating = False
    is_errored = False

    # Alarm timer 
    snooze_countdown = 0

    # Sensor Readings
    setPointReading = 0
    analogTempReading = 0
    ambientSensorReadings = []
    probeReading = 0
    
    heaterStates = []

    physicalControlLine = False
    physicalHeaterCommand = False
    
    # Control Outputs
    soundAlarm = False
    alarmCodes  = {
    "Too Hot": False,
    "Too Cold": False,
    "Heater Malfunction": False,
    "Digital Sensor Disconnect" : False,
    "Control Sensor Malfunction" : False,
    "Temperature Shutdown" : False
    }
    heaterOn = False
    


'''
control sensor
monitor sensor
ambient sensor

- 

making all casing the same
graphics to show plug in locations, if they are in, etc
show trace for temperature
'''