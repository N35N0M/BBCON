from motors import Motors
from camera import Camera
from ultrasonic import Ultrasonic
from reflectance_sensors import ReflectanceSensors

class Sensob():
    def __init__(self,sensor):
        self.sensor = sensor

    def update(self):
        for sensor in self.sensors:
            sensor.update()

    def get_values(self):
        for sensor in self.sensors:


    def reset(self):


class Motob():

class Arbitrator():

