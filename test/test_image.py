import unittest
import image
from config import *

class TestImage(unittest.TestCase):
    def setUp(self):
        self.im = image.loadImage('test\\resource\\test.png')
        self.t = image.loadImage('test\\resource\\i.png')
        pass

    def tearDown(self):
        image.releaseAllWindows()

    def test_loading(self):
        self.assertFalse(self.im is None)
        self.assertFalse(self.t is None)
        with self.assertRaises(FileNotFoundError):
            image.loadImage('test\\resource\\null.png')

    def test_size(self):
        self.assertTrue(
            image.getImageSize(self.im) == (1280, 768) # (x,y)
        )

    def test_exactMatch(self):
        center, v = image.matchTemplateExact(self.im, self.t)
        tsize = image.getImageSize(self.t)
        pt1 = (center[0] - tsize[0] // 2,
               center[1] - tsize[1] // 2)
        pt2 = (center[0] + tsize[0] // 2,
               center[1] + tsize[1] // 2)
        rst = image.drawBox(self.im, pt1, pt2)
        image.showImage(rst)
        self.assertEqual(v, 0)
        self.assertEqual(center, (625, 729))
        self.assertNotEqual(image.waitKeyboard(), -1)



if __name__ == '__main__':
    unittest.main()