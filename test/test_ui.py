import unittest
import image
import getBoxByGui
import api
from config import *

class TestUI(unittest.TestCase):
    def setUp(self):
        self.im = image.loadImage('test\\resource\\test.png')
        pass

    def tearDown(self):
        image.releaseAllWindows()

    def test_getBoxByGui(self):
        pt = getBoxByGui.getBoxByGui(self.im)
        self.assertFalse(pt is None)
        self.assertFalse(pt[0] is None)
        self.assertFalse(pt[1] is None)

    @unittest.skip('progress bar')
    def test_waitFunction(self):
        api.delay(5)
        api.delay(15)
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()