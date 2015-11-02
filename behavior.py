from helper import Sensob
from motors import Motors
from camera import Camera
from ultrasonic import Ultrasonic
from reflectance_sensors import ReflectanceSensors

class Behavior():
    def __init__(self, bbcon, sensobs):
        self.sensobs =
        self.motor_recommendations =
        self.active_flag =
        self.halt_request =
        self.priority =
        self.match_degree =
        self.weight =

    def get_weight(self):
        return self.weight

    def get_halt_request(self):
        return self.halt_request

    def get_motor_recommendations(self):
        return self.motor_recommendations

    def consider_deactivation(self):
        pass

    def consider_activation(self):
        pass

    def update(self):
        pass

    def sense_and_act(self):
        pass
