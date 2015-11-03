from camera import Camera
from helper import Sensob
from ultrasonic import Ultrasonic
from reflectance_sensors import ReflectanceSensors
import logging, sys

from random import randrange

logging.basicConfig(stream=sys.stderr, level=logging.INFO)


class Behavior():
    def __init__(self, BBCON):
        self.motor_recommendations = [0,0]              #A list of numbers, one for each motob, in range [-1,1]
        self.active_flag = False                        #Used to check in the consider methods what it should check for
        self.halt_request = False                       #If set to true, the program (thus robot) should terminate its run
        self.match_degree = 0                           #Number in range [0,1], the degree of how close current conditions are to desired behavior
        self.bbcon = BBCON                              #Reference to the BBCON, mainly for communications such as activate/deactivate

    def get_weight(self):
        return self.weight

    def get_halt_request(self):
        return self.halt_request

    def get_motor_recommendations(self):
        return self.motor_recommendations

    #Checks if the behavior needs to be activated or deactivated according to a predefined test
    #Should be expanded to also deactivate senseobs, but requires bookkeeping to see if it's in other behaviors as well.
    #Maybe have a activeSenseob/senseOb in BBCON, similarily to behaviors?
    def considerState(self):
        if self.active_flag:                #If the behavior is active...
            if not self.test():             #... and if the test fails
                self.active_flag = False    #Deactivate the behavior
                self.bbcon.deactivate_behavior(self)
        else:
            if self.test():
                self.active_flag = True
                self.bbcon.activate_behavior(self)


    def test(self):
        return False #The superclass shouldn't constitute a valid behavior

    # def update(self):
    #     self.considerState()
    #     self.sense_and_act()
    #     self.weight = self.priority * self.match_degree
    #
    # def sense_and_act(self):
    #     pass #Highly specialized method
    # __update = update
    # __sense = sense_and_act

class PictureWhenClose(Behavior):
    def __init__(self, BBCON, priority):
        super().__init__(BBCON)
        self.sensobs = [Sensob(Camera(img_height=1920,img_width=1080)), Sensob(Ultrasonic())]
        self.priority = priority                      #Preset value that is set by the user
        self.picTaken = False
        for sensob in self.sensobs:
            sensob.update()

    def printName(self):
        return "Behavior PictureWhenClose"

    #Update is executed in three steps (one if deactivated):
    # 1) Check to see if it should be active, 2) sense and act, 3) calculate weight
    def update(self):
        super().considerState()

        if self.active_flag:
            self.sense_and_act()
            self.weight = self.priority * self.match_degree


    def test(self):
        if (self.sensobs[1].get_value() > 70):
            return False
        else:
            return True

    def sense_and_act(self):
        cameraData = self.sensobs[0].get_value()
        cameraData.save("result.png")
        self.picTaken = True
        self.halt_request = True
        self.match_degree = 1
        # faceCascade = cv2.CascadeClasifier('haarcascade_frontalface_default.xml')
        # cvimage = cv2.imread('image.png')
        # gray = cv2.cvtColor(cvimage, cv2.COLOR_BGR2GRAY)
        # faces = faceCascade.detectMultiScale(
        #     gray,
        #     scaleFactor=1.1,
        #     minNeighbors=5,
        #     minSize=(30, 30),
        #     flags = cv2.cv.CV_HAAR_SCALE_IMAGE
        # )
        # if faces is not 0:
        #     cv2.imwrite('FACE.jpg')
        #
        # else:
        #     pass

class RandomWalk(Behavior):
    def __init__(self, BBCON, priority):
        super().__init__(BBCON)
        self.sensobs = []
        self.priority = priority                      #Preset value that is set by the user
        self.randomCount = 0
        for sensob in self.sensobs:
            sensob.update()

    def printName(self):
        return "Behavior random walk"

    #Update is executed in three steps (one if deactivated):
    # 1) Check to see if it should be active, 2) sense and act, 3) calculate weight
    def update(self):
        super().considerState()

        if self.active_flag:
            self.sense_and_act()
            self.weight = self.priority * self.match_degree


    def test(self):
        return True

    def sense_and_act(self):
        if self.randomCount%2 == 0:
            self.motor_recommendations = (1,1)
        else:
            randomNumber1 = randrange(-10,10,1)/10
            randomNumber2 = randrange(-10,10,1)/10

            print(randomNumber1,randomNumber2)

            self.motor_recommendations = [randomNumber1,randomNumber2]

        self.randomCount += 1

        self.match_degree = 1