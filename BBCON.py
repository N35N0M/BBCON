import Arbitrator           #Arbitrator class
import Behavior             #Behavior class
import ultrasonic           #SenseObj
import reflectance_sensors  #SenseObj
import camera               #SenseObj
import zumo_button          #Contains ZumoButton-class w/ wait_for_press method
from filename import classname
import time

##Implents a Behavior Based Controller for Robotics Control
class BBCON():


    def __init__(self, timesteplength):
        behaviors = []
        activeBehaviors = []
        sensobs = []
        motobs = []
        self.timesteplength = timesteplength
        arbitrator = Arbitrator()

    #Appends a behavior object to a list
    def add_behavior(self, behavior):
        self.behaviors.append(behavior)

    #Appends a sense object to a list
    def add_senseob(self,senseob):
        self.senseobs.append(senseob)

    #Appends a behavior to a list
    def activate_behavior(self, behavior):
        if behavior in self.behaviors:
            self.activeBehaviors.append(behavior)

    #Removes a behavior from a list
    def deactivate_behavior(self, behavior):
        if behavior in self.active_behaviors:
            self.activeBehaviors.remove(behavior)

    #IN PROGRESS
    def run_one_timestep(self):
        self.update_senseobs()
        self.update_behaviors()
        self.arbitrator.choose_action()
        self.update_motobs()
        time.sleep(self.timesteplength)
        self.reset_sensobs()

    #Updates the values for each sense object, called at each timestep
    def update_senseobs(self):
        for sense in self.senseobs:
            sense.update()

    #Updates the values for each behavior object, called at each timestep
    def update_behaviors(self):
        for behavior in self.behaviors:
            behavior.update()

    def update_motobs(self):
        for motor in self.motobs:
            motor.update()

    def reset_sensobs(self):
        for sense in self.senseobs:
            sense.reset()