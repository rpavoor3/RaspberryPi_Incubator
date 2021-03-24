import random
class Patient():
  tempSensor   = None

  def __init__(self):
    tempSensor = 0

  def temperature(self):

    return random.randint(0, 35)

  def temp_warning(self):
    temp = self.tempSensor.temperature

    if temp < 36.0:
      return True
    elif temp > 37.5:
      return True
    else:
      return False
