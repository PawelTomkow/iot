import logging

logging.basicConfig(format='[%(asctime)s][%(levelname)s]: %(message)s', level=logging.DEBUG)

def start_debug():
    logging.debug("----------- Start debug message ------------")

def end_debug():
    logging.debug("----------- End debug message ------------")

def info_log(message):
    logging.info(message)


def error(param):
    logging.error(param)