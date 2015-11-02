from zumo_button import ZumoButton          #Contains ZumoButton-class w/ wait_for_press method
from BBCON import BBCON

import logging, sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def main():
    logging.debug("Main method initiated, waiting for button press")
    ZumoButton().wait_for_press()

    timeStep = 1

    Controller = BBCON(timeStep)
    Controller.run_one_timestep()

    logging.debug("Main method terminated without error")


main()
