import numpy as np
import image
import tqdm
import time
import device
import log
import resource.cache as cache
import logging
import resource
import math
from config import *

class Scenario(object):

    name = 'Scenario'  # Name of this scenario

    #  Access if a given image fits this scenario
    @classmethod
    def isMatch(cls, img:np.ndarray):
        return False

def ToBaseScene():
    raise NotImplementedError('ToBaseSecene() API Not implemented')

def identifyLocation(img, template, threshold = 5):
    centre, v = image.matchTemplateExact(img, template)
    if v > threshold: return None
    return centre


def delay(s=5, m=0, h=0):
    logger = logging.getLogger(__name__)
    t = s + m *60 + h * 3600
    logger.info('Request Delaying %s seconds' % t)
    if (t <= 10):
        t *= 100
        for i in tqdm.trange(t):
            time.sleep(0.01)
    else:
        for i in tqdm.trange(t):
            time.sleep(1)
    logger.info('Resume Execution...')

def touchAt(location):
    logger = logging.getLogger(__name__)
    logger.info('Request Touch At Location (%d, %d)' % location)
    device.simulateTouch(location[0], location[1])

def getScreenshot():
    logger = logging.getLogger(__name__)
    logger.info('Request Snapshot')
    d = device.SnapFetcher()
    d.screenShot()
    loc = config['snapshot']['localPath']
    im = image.loadImage(loc)
    return im

def loadImageByKey(scene, key):
    logger = logging.getLogger(__name__)
    logger.info('Request to load Image "%s" => "%s' % (scene, key))
    return cache.cacheLoadImage(scene, key)
    #return image.loadResourceImage(resource.images[scene][key])


def isAround(pt1, pt2, dis=30):
    dx = pt1[0] - pt2[0]
    dy = pt1[1] - pt2[1]
    return math.sqrt(dx * dx + dy * dy) <= dis


def creatLogger(name):
    # create logger
    logger = logging.getLogger('Task {%s}' % name)
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    fch = logging.FileHandler(config['logging']['path'] + 'Task_' + name + '.log')
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

    return logger

def getLogger(name):
    return logging.getLogger('Task {%s}',name)

def retry(t):
    i = 0
    while i < t:
        yield i
        i += 1
    raise RuntimeError('Retry gives up')