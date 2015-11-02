from motors import Motors
from camera import Camera
from ultrasonic import Ultrasonic
from reflectance_sensors import ReflectanceSensors

## A Sensob can contain multiple sensor references, to be used in behaviors.
class Sensob():
    ## Constructor that initiates a senseob with all neccessary sensors
    def __init__(self,sensors):
        self.sensors = sensors

    ## Makes each sensor associated with the senseob measure a new value
    def update(self):
        for sensor in self.sensors:
            sensor = sensor.update()

    ## Gets the most recently measured value from each sensor
    def get_values(self):
        values = []
        for sensor in self.sensors:
            values.append(sensor.get_value())

        return values

    ## Resets each sensor, setting each value to None or -1, etc
    def reset(self):
        for sensor in self.sensors:
            sensor.reset()


## Motor object. Contains several motor references and has the power to operationalize
## all the motors it references
class Motob():

    #Constructor
    def __init__(self, motors, value=0):
        self.motors = motors    #Apparantly a list of motors
        self.value = value      #The latest motor recommendation sent

    #Updates the motor recommendation, and operationalizes it.
    def update(self, motorValue):
        self.value = motorValue
        self.operationalize()

    def operationalize(self):
        ## Every motor can have a value between [-1,1]
        ## Perhaps we should error-check to see if it's in range?
        v = self.value

        for motor in self.motors:
            if v == 0:
                motor.stop()
            else:
                motor.set_value(v)

## Chooses a behavior (highest weight or stochastic choice), and returns
## a motor recommendation and halt-entirely boolean as a tuple.
class Arbitrator():

    ##Initiates with reference to BBCON (and its behaviors)
    ##Stochastic decides whether or not this is a stochastic Arbitrator
    def __init__(self, BBCON, stochastic=False):
        self.BBCON = BBCON

        if stochastic:
            self.choose_action_stochastic()
        else:
            self.choose_action()

    def choose_action(self):
        behaviors = self.BBCON.get_activeBehaviors()
        maxWeight = -float("Inf")
        winningBehavior = None

        for b in behaviors:
            weight = b.get_weight()

            if weight > maxWeight:
                maxWeight = weight
                winningBehavior = b

        if maxWeight != -float("Inf") and winningBehavior:       #If both values are set...
            return (winningBehavior.get_motor_recommendations(), winningBehavior.get_halt_request())





    def choose_action_stochastic(self):
        pass


