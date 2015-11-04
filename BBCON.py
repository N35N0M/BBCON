from helper import Arbitrator, Motob           #Arbitrator class
from time import sleep
import logging, sys
from motors import Motors


logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


#DEBUG example: logging.debug('A debug message!')
#INFO example: logging.info('We processed %d records', len(processed_records))
#Other modes: WARNING, ERROR, CRITICAL

##Implents a Behavior Based Controller for Robotics Control
class BBCON():
    def __init__(self, timesteplength):
        self.behaviors = []                         #List of all behaviors
        self.activeBehaviors = []                   #List of all behaviors currently monitored
        self.senseobs = []                           #List of all unique sensobs, for updating
        self.motob = Motob(Motors())                            #List of all unique motobs
        self.timesteplength = timesteplength        #Time step (how often the robot should choose a new action)
        self.arbitrator = Arbitrator(self,False)    #Arbitrator
        self.halt = False

        logging.debug("Behavior-based Controller initialized")

    def get_activeBehaviors(self):
        return self.activeBehaviors

        logging.debug("Active behaviors retrieved")

    #Appends a behavior object to a list
    def add_behavior(self, behavior):
        self.behaviors.append(behavior)

        logging.debug("Behavior added to behavior list")

    #Appends a sense object to a list
    def add_senseob(self,senseob):
        self.senseobs.append(senseob)

        logging.debug("Senseob added to senseob list")

    #Appends a behavior to a list
    def activate_behavior(self, behavior):
        if behavior in self.behaviors:
            self.activeBehaviors.append(behavior)
            logging.debug("Behavior activated")

    #Removes a behavior from a list
    def deactivate_behavior(self, behavior):
        if behavior in self.active_behaviors:
            self.activeBehaviors.remove(behavior)
            logging.debug("Behavior deactivated")

    #IN PROGRESS
    def run_one_timestep(self):
        logging.debug("==== RUNNING TIMESTEP ====")
        self.update_senseobs()
        self.update_behaviors()
        arbitratorsChoice = self.arbitrator.choose_action()

        if arbitratorsChoice[1]:   #If halt_request is true
            self.halt = True
            self.update_motobs(0)
            logging.debug("HALT REQUESTED!")
        elif arbitratorsChoice == (None,None):
            pass
        else:
            #self.update_motobs(arbitratorsChoice[0]*0.1)
            self.update_motobs([x*1 for x in arbitratorsChoice[0]])

        sleep(self.timesteplength)
        self.reset_sensobs()

        logging.debug("==== TIMESTEP RUN SUCCESSFUL ====")

    #Updates the values for each sense object, called at each timestep
    def update_senseobs(self):
        for sense in self.senseobs:
            sense.update()

        logging.debug("Senseobs updated")

    #Updates the values for each behavior object, called at each timestep
    def update_behaviors(self):
        for behavior in self.behaviors:
            behavior.update()

        logging.debug("Behaviors updated")

    def update_motobs(self, value):
        self.motob.update(value)
        logging.debug("Motobs updated")

    def reset_sensobs(self):
        for sense in self.senseobs:
            sense.reset()

        logging.debug("Senseobs reset")


