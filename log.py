import logging

from config import *

def setScreenShotLogger():
    # create logger
    logger = logging.getLogger('screenshot')
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    fch = logging.FileHandler(config['logging']['file'])
    ch.setLevel(logging.DEBUG)
    fch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)
    fch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
    logger.addHandler(fch)


def setImageLogger():
    # create logger
    logger = logging.getLogger('image')
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    fch = logging.FileHandler(config['logging']['file'])
    ch.setLevel(logging.DEBUG)
    fch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)
    fch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
    logger.addHandler(fch)

def setApiLogger():
    # create logger
    logger = logging.getLogger('api')
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    fch = logging.FileHandler(config['logging']['file'])
    ch.setLevel(logging.DEBUG)
    fch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)
    fch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
    logger.addHandler(fch)



setScreenShotLogger()
setImageLogger()
setApiLogger()