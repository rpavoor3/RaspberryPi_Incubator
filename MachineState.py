class MachineState:

    # Push button managed states
    is_snoozed = False
    is_preheat = False

    # Sensor Readings
    setPointReading = 0
    analogTempReading = 0
    ambientSensorReadings = []
    probeReading = 0
    batteryStatus = False
    heaterHealth = None
    
    # Control Outputs
    alarmStatus = False
    alarmCodes  = {
    "Too Hot": False,
    "Too Cold": False,
    "Heater Malfunction": False,
    "Digital Sensor Disconnect" : False,
    "Control Sensor Malfunction" : False
    }
    heaterOn = False





