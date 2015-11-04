from zumo_button import ZumoButton          #Contains ZumoButton-class w/ wait_for_press method
from BBCON import BBCON
from helper import Sensob
from motors import Motors
from camera import Camera
from ultrasonic import Ultrasonic
from reflectance_sensors import ReflectanceSensors
from behavior import Behavior, PictureWhenClose, RandomWalk, AvoidEdge
import logging, sys


logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

if __name__=="__main__":
    logging.debug("Main method initiated, waiting for button press")
    ZumoButton().wait_for_press()

    timeStep = 0.5

    #Create controller and add behaviors
    Controller = BBCON(timeStep)
    Controller.add_behavior(PictureWhenClose(Controller, 1))
    Controller.add_behavior(RandomWalk(Controller,0.3))
    Controller.add_behavior(AvoidEdge(Controller,1))

    while(not Controller.halt):
        Controller.run_one_timestep()

    logging.debug("Main method terminated without error")
