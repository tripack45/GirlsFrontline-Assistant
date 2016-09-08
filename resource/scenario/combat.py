import api
import numpy as np
import logging


class SceneCombat(api.Scenario):

    name = 'Combat (Main Scene)'

    @classmethod
    def isMatch(cls, img:np.ndarray):
        text = api.loadImageByKey('combat', 'text')
        iconGK = api.loadImageByKey('combat', 'iconGK')
        buttonReturn = api.loadImageByKey('combat', 'buttonReturn')
        match = api.identifyLocation(img, text)
        if match is None: return False
        if not api.isAround(match, (247, 52)): return False
        match = api.identifyLocation(img, iconGK)
        if match is None: return False
        if not api.isAround(match, (96, 634)): return False
        match = api.identifyLocation(img, buttonReturn)
        if match is None: return False
        if not api.isAround(match, (73, 49)): return False
        return True

    @classmethod
    def getButtonMap1_2(cls, img):
        button = api.loadImageByKey('combat', 'buttonBattle1-2')
        match = api.identifyLocation(img, button)
        return match

    @classmethod
    def buttonReturnBase(cls):
        return (57, 40)


class CombatSetting(api.Scenario):

    name = 'Combat (setting)'

    @classmethod
    def isMatch(cls, img:np.ndarray):
        title           = api.loadImageByKey('combatSetting', 'title')
        text            = api.loadImageByKey('combatSetting', 'text')
        buttonAuto      = api.loadImageByKey('combatSetting', 'buttonAutoCombat')
        buttonNormal    = api.loadImageByKey('combatSetting', 'buttonNormalCombat')
        match = api.identifyLocation(img, title)
        if match is None: return False
        if not api.isAround(match, (359, 122)): return False
        match = api.identifyLocation(img, text)
        if match is None: return False
        if not api.isAround(match, (408, 602)): return False
        match = api.identifyLocation(img, buttonAuto)
        if match is None: return False
        if not api.isAround(match, (682, 603)): return False
        match = api.identifyLocation(img, buttonNormal)
        if match is None: return False
        if not api.isAround(match, (883, 602)): return False
        return True

    @classmethod
    def selectAutoCombat(cls):
        return (685, 600)

    @classmethod
    def selectNormalCombat(cls):
        return (880, 600)


class AutoCombatSelectTeam(api.Scenario):

    name = 'Auto combat (setting)'

    @classmethod
    def isMatch(cls, img:np.ndarray):
        title           = api.loadImageByKey('autoCombatSetting', 'title')
        text            = api.loadImageByKey('autoCombatSetting', 'infoText')
        buttonConfirm   = api.loadImageByKey('autoCombatSetting', 'confirm')
        match = api.identifyLocation(img, title)
        if match is None: return False
        if not api.isAround(match, (361, 122)): return False
        match = api.identifyLocation(img, text, 3)
        if match is None: return False
        #if not api.isAround(match, (408, 602)): return False
        match = api.identifyLocation(img, buttonConfirm)
        if match is None: return False
        if not api.isAround(match, (992, 602)): return False
        return True

    @classmethod
    def beginSelectTeam(cls):
        # Currently support only single team
        return (635, 328)

    @classmethod
    def hasEmptySlot(cls, img):
        slot = api.loadImageByKey('autoCombatSetting', 'emptySlot')
        match = api.identifyLocation(img, slot, 2)
        if match is None: return False

    @classmethod
    def confirmSelection(cls):
        return (1020, 590)


class TeamSelection(api.Scenario):

    name = 'Team Selection'

    @classmethod
    def isMatch(cls, img:np.ndarray):
        title           = api.loadImageByKey('TeamSelection', 'title')
        cancelConfirm   = api.loadImageByKey('TeamSelection', 'cancelConfirm')
        match = api.identifyLocation(img, title)
        if match is None: return False
        if not api.isAround(match, (287, 137)): return False
        match = api.identifyLocation(img, cancelConfirm)
        if match is None: return False
        if not api.isAround(match, (1087, 662)): return False
        return True

    @classmethod
    def Team2(cls, img):
        tag2 = api.loadImageByKey('TeamSelection', 'tag2')
        match = api.identifyLocation(img, tag2, 3)
        return match

    @classmethod
    def Team2Selected(self, img):
        tag2Sel = api.loadImageByKey('TeamSelection', 'tag2Selected')
        match = api.identifyLocation(img, tag2Sel, 3)
        return match

    @classmethod
    def SelectConfirm(cls):
        return (1170, 660)

