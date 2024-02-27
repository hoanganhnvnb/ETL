import os
import sys

try:
    sys.path.append(os.path.dirname(os.path.realpath(__file__)))
except Exception as e:
    print("Error: " + str(e))

from controller.controller import Controller

if __name__ == '__main__':
    # get data from configuration file

    controller = Controller()
    controller.start()