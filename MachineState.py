class MachineState:

    # Push button managed states
    is_snoozed = False
    is_snooze_requested = False
    is_preheating = False

    # Sensor Readings
    setPointReading = 0
    analogTempReading = 0
    ambientSensorReadings = []
    probeReading = 0
    batteryStatus = False
    heaterHealth = []
    
    # Control Outputs
    soundAlarm = False
    alarmCodes  = {
    "Too Hot": False,
    "Too Cold": False,
    "Heater Malfunction": False,
    "Digital Sensor Disconnect" : False,
    "Control Sensor Malfunction" : False
    }
    heaterOn = False
    





