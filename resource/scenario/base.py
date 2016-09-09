import api
import numpy as np
import logging as log
import image

class SceneBaseNormal(api.Scenario):

    name = 'Base Scene (Normal)'

    @classmethod
    def isMatch(cls, img:np.ndarray):
        t = api.loadImageByKey('base', 'buttonCombat')
        c, v = image.matchTemplateExact(img, t)
        if v >= 5 or (not api.isAround(c, (924, 535))):
            return False
        t = api.loadImageByKey('base', 'iconMoreResource')
        c, v = image.matchTemplateExact(img, t)
        if v >= 5 or (not api.isAround(c, (1252, 28))):
            return False
        t = api.loadImageByKey('base', 'playerName')
        c, v = image.matchTemplateExact(img, t)
        if v >= 5 or (not api.isAround(c, (144, 33))):
            return False
        t = api.loadImageByKey('base', 'iconStore')
        c, v = image.matchTemplateExact(img, t)
        if v >= 5 or (not api.isAround(c, (902, 728))):
            return False
        return True

    @classmethod
    def getButtonShowTime(cls, img=None):
        return (15, 378)

    @classmethod
    def getButtonCombat(cls, img=None):
        return (930, 540)


class ScenceBaseTime(api.Scenario):

    name = 'Base Scene (With Time)'

    @classmethod
    def getButtonCloseTime(cls, img=None):
        return (777, 381)