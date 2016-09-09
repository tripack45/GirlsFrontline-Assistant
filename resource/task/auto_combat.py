import api
import image
import resource.scenario.base as base
import resource.scenario.combat as combat

# Continuously Select Team2 To Auto Combat on Map 1-2
# Must start with the home screen

logger = api.creatLogger('AutoCombat')

def transition(prevScene, nextScene, actionCoords):
    global logger
    img = api.getScreenshot()
    if not nextScene.isMatch(img):
        logger.warning(nextScene.name + ' not found')
        try:
            for i in api.retry(5):
                logger.info('Retry %d ...' % i)
                if i >= 3:
                    api.touchAt(250, 250)
                api.delay(3)
                img = api.getScreenshot()
                if nextScene.isMatch(img):
                    break
                elif prevScene.isMatch(img):
                    api.touchAt(actionCoords)
        except RuntimeError:
            logger.error('Cannot enter ' + nextScene.name)
            raise
    logger.info(nextScene.name + ' Found')
    return img

def setup():
    global logger
    logger.info('============== Started ============')
    img = api.getScreenshot()
    if not base.SceneBaseNormal.isMatch(img):
        logger.warning('Base Scene not found')
        try:
            for i in api.retry(5):
                logger.info('Retry %d ...' % i)
                if i >= 3:
                    api.touchAt((250, 250))
                api.delay(3)
                img = api.getScreenshot()
                if base.SceneBaseNormal.isMatch(img):
                    break
        except RuntimeError:
            logger.error('Cannot find Base Scene')
            raise
    logger.info('Found Base Scene')

def do():
    global logger
    buttonCombat = base.SceneBaseNormal.getButtonCombat()
    api.touchAt(buttonCombat)
    logger.info('Simulate TouchAt(ButtonCombat)')
    api.delay(3)

    img = transition(base.SceneBaseNormal,
                     combat.SceneCombat,
                     buttonCombat)
    logger.info('Trying to identify "buttonMap1_2"')
    buttonMap1_2 = combat.SceneCombat.getButtonMap1_2(img)
    if buttonMap1_2 is None:
        try:
            for i in api.retry(5):
                logger.info('Retry %d ...' % i)
                if i >= 3:
                    api.touchAt(250, 250)
                api.delay(3)
                img = api.getScreenshot()
                buttonMap1_2 = combat.SceneCombat.getButtonMap1_2(img)
                if not (buttonMap1_2 is None):
                    break
        except RuntimeError:
            image.writePNG('Bug.png',img)
            logger.error('Cannot Identify')
            raise
    logger.info('Button Identified')
    api.touchAt(buttonMap1_2)
    logger.info('Simulate TouchAt(buttonMap1_2)')
    api.delay(1)

    img = transition(combat.SceneCombat,
                     combat.CombatSetting,
                     buttonMap1_2)
    buttonAuto = combat.CombatSetting.selectAutoCombat()
    api.touchAt(buttonAuto)
    logger.info('Simulate TouchAt(buttonAuto)')
    api.delay(1)

    img = transition(combat.CombatSetting,
                     combat.AutoCombatSelectTeam,
                     buttonMap1_2)
    buttonSelect = combat.AutoCombatSelectTeam.beginSelectTeam()
    api.touchAt(buttonSelect)
    logger.info('Simulate TouchAt(buttonSelect)')
    api.delay(1)

    img = transition(combat.AutoCombatSelectTeam,
                     combat.TeamSelection,
                     buttonMap1_2)
    logger.info('Trying to identify "tag2"')
    tag2 = combat.TeamSelection.Team2(img)
    tag2Sel = combat.TeamSelection.Team2Selected(img)
    if (tag2 is None) and (tag2Sel is None):
        try:
            for i in api.retry(5):
                logger.info('Retry %d ...' % i)
                if i >= 3:
                    api.touchAt(250, 250)
                api.delay(3)
                img = api.getScreenshot()
                tag2 = combat.TeamSelection.Team2(img)
                tag2Sel = combat.TeamSelection.Team2Selected(img)
                if not ((tag2 is None) and (tag2Sel is None)):
                    break
        except RuntimeError:
            logger.error('Cannot Identify')
            raise
    if tag2Sel is None:
        logger.info('Button Identified')
        api.touchAt(tag2)
        logger.info('Simulate TouchAt(tag2)')
        api.delay(1)
    else:
        logger.info('Tag2 already selected')

    img = api.getScreenshot()
    if not (combat.TeamSelection.Team2Selected(img)):
        logger.warning('Retry simulate TouchAt(tag2)')
        try:
            for i in api.retry(5):
                logger.info('Retry %d ...' % i)
                if i >= 3:
                    api.touchAt(250, 250)
                api.delay(3)
                img = api.getScreenshot()
                if combat.TeamSelection.Team2Selected(img):
                    break
                elif combat.TeamSelection.Team2(img):
                    api.touchAt(tag2)
        except RuntimeError:
            logger.error('Cannot select team2!')
            raise
    logger.info('Team 2 Selected')
    buttonYes = combat.TeamSelection.SelectConfirm()
    api.touchAt(buttonYes)
    logger.info('touchAt(buttonYes)')
    logger.info('Confirming Team 2 Selection')

    img = transition(combat.TeamSelection,
                     combat.AutoCombatSelectTeam,
                     buttonYes)
    logger.info('Team 2 Selection Confirmed')
    hasSlot = combat.AutoCombatSelectTeam.hasEmptySlot(img)
    if not hasSlot:
        logger.info('No empty slot, we can begin')
    else:
        logger.error('Unknow Error')
        raise RuntimeError('Unknown Error')

    buttonBeginAuto = combat.AutoCombatSelectTeam.confirmSelection()
    api.touchAt(buttonBeginAuto)
    logger.info('touchAt(buttonBeginAuto)')
    logger.info('Confirming Operation...')

    api.delay(5)
    img = transition(combat.AutoCombatSelectTeam,
                     combat.SceneCombat,
                     buttonBeginAuto)

    logger.info('Operation Confirmed')
    logger.info('Returning to Base...')

    buttonReturnBase = combat.SceneCombat.buttonReturnBase()
    api.touchAt(buttonReturnBase)
    logger.info('touchAt(buttonReturnBase)')

    api.delay(3)
    img = transition(combat.AutoCombatSelectTeam,
                     base.SceneBaseNormal,
                     buttonReturnBase)
    logger.info('Now We Wait 10 Minutes')
    api.delay(s = 0, m=10)

    img = api.getScreenshot()
    while not base.SceneBaseNormal.isMatch(img):
        img = api.getScreenshot()
        api.touchAt((250, 250))
        api.delay(3)

    logger.info('==========Congratualations!=======')

if __name__ == '__main__':
    setup()
    while True:
        try:
            do()
        except RuntimeError:
            api.touchAt((250, 250))
