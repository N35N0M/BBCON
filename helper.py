from random import randint
import logging, sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

## A Sensob can contain multiple sensor references, to be used in behaviors.
class Sensob():
    ## Constructor that initiates a senseob with all neccessary sensors
    def __init__(self,sensor):
        self.sensor = sensor
        logging.debug("Senseob created")

    ## Makes each sensor associated with the senseob measure a new value
    def update(self):
        sensor = self.sensor.update()

        logging.debug("Senseob updated")

    ## Gets the most recently measured value from each sensor
    def get_value(self):
        logging.debug("Values retrieved")
        return self.sensor.get_value()

    ## Resets each sensor, setting each value to None or -1, etc
    def reset(self):
        self.sensor.reset()
        logging.debug("Senseob reset")


## Motor object. Contains several motor references and has the power to operationalize
## all the motors it references
class Motob():
    #Constructor
    def __init__(self, motor, value=None):
        self.motor = motor    #Apparantly a list of motors
        self.value = value      #The latest motor recommendation sent

        logging.debug("Motob created")

    #Updates the motor recommendation, and operationalizes it.
    def update(self, motorValue):
        self.value = motorValue
        logging.debug("Motob value updated")
        self.operationalize()

    #Gives each motor in the motob a new setting
    def operationalize(self):
        ## Every motor can have a value between [-1,1]
        ## Perhaps we should error-check to see if it's in range?
        v = self.value

        if v == 0:
            self.motor.stop()
        else:
            self.motor.set_value(v)

        logging.debug("Motob operationalized")

## Chooses a behavior (highest weight or stochastic choice), and returns
## a motor recommendation and halt-entirely boolean as a tuple.
class Arbitrator():

    ##Initiates with reference to BBCON (and its behaviors)
    ##Stochastic decides whether or not this is a stochastic Arbitrator
    def __init__(self, BBCON, stochastic=False):
        self.BBCON = BBCON
        self.behaviors = BBCON.get_activeBehaviors()

        self.stochastic = stochastic

        logging.debug("Arbitrator initiated")



    #Chooses an action based on the one with the highest weight.
    #RETURNs tuple with (motor_recommendation, haltflag), or (None, None) if there is an error or
    #no best COA is found

    #Choose_action and stochastic must be combined with if-structure
    def choose_action(self):
        self.behaviors = self.BBCON.get_activeBehaviors()

        if not self.stochastic:
            logging.debug("Normal choose_action called")
            maxWeight = -float("Inf")
            winningBehavior = None

            for b in self.behaviors:
                weight = b.get_weight()

                if weight > maxWeight:
                    maxWeight = weight
                    winningBehavior = b

            if maxWeight != -float("Inf") and winningBehavior:       #If both values are set...
                logging.debug("Arbitrator has chosen an action!")
                return (winningBehavior.get_motor_recommendations(), winningBehavior.get_halt_request())
            else:
                logging.debug("Uhoh! Arbitrator wasn't able to chose an action!")
                return (None,None)    #Perhaps throw an error or print something? This indicates that there are no
                        #active behaviors or there's something wrong with the code (or both!)
        else:
            logging.debug("Stochastic choose_action called.")
            range = 0
            rangeTable = []
            chosenBehavior = None

            for b in self.behaviors:
                range += b.get_weight()
                rangeTable.append(range)

            stochasticVariable = randint(0,range)

            for i in range(len(rangeTable)):
                if rangeTable[i] >= stochasticVariable:
                    chosenBehavior = self.behaviors[i]
                    break

            if chosenBehavior is not None:
                logging.debug("Stochastic arbitrator has chosen an action!")
                return (chosenBehavior.get_motor_recommendations(), chosenBehavior.get_halt_request())
            else:
                logging.debug("Uhoh! Stochastic arbitrator wasn't able to chose an action")
                return (None, None)    ## No behavior found? Throw error or some system warning?








