from zumo_button import ZumoButton          #Contains ZumoButton-class w/ wait_for_press method

def main():
    ZumoButton().wait_for_press()
    print ("Main ended successfully!")

main()
