import unittest
import os
from glob import glob
import image
import api
import resource.scenario.base as base
import resource.scenario.combat as combat


class TestScene(unittest.TestCase):

    imgList = {}

    @classmethod
    def setUpClass(cls):
        file = glob('test\\resource\\*.png')
        cls.imgList = {}
        for f in file:
            cls.imgList[f] = image.loadImage(f)

    def testBase(self):
        trueList = ('base.png',
                    'base_with_mail.png',
                    'base_without_mail.png')
        for image in TestScene.imgList:
            predicate = base.SceneBaseNormal.isMatch(TestScene.imgList[image])
            with self.subTest(image=image):
                head, tail = os.path.split(image)
                if tail in trueList:
                    self.assertTrue(predicate)
                else:
                    self.assertFalse(predicate)

    def testCombat(self):
        trueList = ('combat.png',
                    'combat2.png',
                    'combat3.png',
                    'combat4.png',
                    'auto1_2_underway.png',
                    'auto1_2_underway2.png')
        for image in TestScene.imgList:
            predicate = combat.SceneCombat.isMatch(TestScene.imgList[image])
            with self.subTest(image=image):
                head, tail = os.path.split(image)
                if tail in trueList:
                    self.assertTrue(predicate)
                else:
                    self.assertFalse(predicate)

    def testCombatLocateB1_2(self):
        for image in TestScene.imgList:
            coords = combat.SceneCombat.\
                getButtonMap1_2(TestScene.imgList[image])
            with self.subTest(image=image):
                head, tail = os.path.split(image)
                if tail == 'combat.png':
                    self.assertTrue(api.isAround(coords, (637, 396)))
                elif tail == 'combat2.png':
                    self.assertTrue(api.isAround(coords, (637, 318)))
                elif tail == 'combat4.png':
                    self.assertTrue(api.isAround(coords, (637, 396)))
                elif tail == 'auto1_2_underway2.png':
                    self.assertTrue(api.isAround(coords, (637, 396)))
                elif tail == 'auto1_2_underway.png':
                    self.assertTrue(api.isAround(coords, (637, 396)))
                elif tail == 'auto1_2_intro.png':
                    self.assertTrue(api.isAround(coords, (437, 222)))
                elif tail == 'auto1_2_intro2.png':
                    self.assertTrue(api.isAround(coords, (437, 222)))
                else:
                    self.assertIs(coords, None)

    def testCombatSetting(self):
        trueList = ('auto1_2_select.png',
                    'auto1_2_select2.png')
        for image in TestScene.imgList:
            predicate = combat.AutoCombatSelectTeam.isMatch(
                TestScene.imgList[image])
            with self.subTest(image=image):
                head, tail = os.path.split(image)
                if tail in trueList:
                    self.assertTrue(predicate)
                else:
                    self.assertFalse(predicate)

    def testTeamSelection(self):
        trueList = ('auto1_2_select_team.png',
                    'auto1_2_select_team2.png')
        for image in TestScene.imgList:
            predicate = combat.TeamSelection.isMatch(
                TestScene.imgList[image])
            with self.subTest(image=image):
                head, tail = os.path.split(image)
                if tail in trueList:
                    self.assertTrue(predicate)
                else:
                    self.assertFalse(predicate)

if __name__ == '__main__':
    unittest.main()