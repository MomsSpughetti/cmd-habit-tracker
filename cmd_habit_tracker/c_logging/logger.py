# importing module
import logging


def start_logger():
    # Create and configure logger
    logging.basicConfig(filename="history.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')

def logger():
    # Creating an object
    return logging.getLogger()

def set_level_debug():
    # Setting the threshold of logger to DEBUG
    logger().setLevel(logging.DEBUG)



