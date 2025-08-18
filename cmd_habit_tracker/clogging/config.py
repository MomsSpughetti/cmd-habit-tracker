# importing module
import logging
from cmd_habit_tracker.utils import data

def start_logger():
    # Create and configure logger
    logging.basicConfig(filename=data.LOGFILE,
                        format='%(asctime)s %(message)s',
                        filemode='w')

def logger():
    # Creating an object
    return logging.getLogger()

def set_level_debug():
    # Setting the threshold of logger to DEBUG
    logger().setLevel(logging.DEBUG)



