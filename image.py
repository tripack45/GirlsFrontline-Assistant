import numpy as np
import cv2
import logging
import enum

from config import *

lastImported = None


class ColorName(enum.Enum):
    ALPHA = 4
    RED = 1
    GREEN = 2
    BLUE = 3


def loadImage(fullpath, option=cv2.IMREAD_COLOR) -> np.ndarray:
    logger = logging.getLogger(__name__)
    logger.info('Loading image "%s"' % fullpath)
    global lastImported
    lastImported = cv2.imread(fullpath, option)
    if lastImported is None:
        logger.error('Failed to load image')
        raise FileNotFoundError('Image not found or not exist')
    else:
        logger.info('Successfully loaded')
    return lastImported


def loadResourceImage(filename, option=cv2.IMREAD_COLOR) -> np.ndarray:
    prefix = config['resource']['path']
    return loadImage(prefix + filename, option)


def getImageSize(image: np.ndarray):
    return (image.shape[1], image.shape[0])


def extractColorChannel(image: np.ndarray, color: ColorName) -> np.ndarray:
    if color == ColorName.RED:
        return image[..., 2].copy()
    if color == ColorName.GREEN:
        return image[..., 1].copy()
    if color == ColorName.BLUE:
        return image[..., 0].copy()
    if color == ColorName.ALPHA:
        if image.ndim < 3:
            errmsg = 'Image does not contain alpha, cannot extract Alpha'
            logging.getLogger(__name__).error(errmsg)
            raise ValueError(errmsg)
        return image[..., 3].copy()


def Bgr2Gray(image) -> np.ndarray:
    im = image.copy()
    if im.ndim < 3:
        return cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    return cv2.cvtColor(im, cv2.COLOR_BGRA2GRAY)


def writePNG(filename, image):
    if image is None:
        logging.getLogger(__name__).error('Writing empty image')
        raise ValueError('Writing empty image')
    cv2.imwrite(filename, image)


def waitKeyboard(ms=0, s=0, m=0, h=0):
    t = 0
    t = (t + h) * 60
    t = (t + m) * 60
    t = (t + s) * 1000
    t += ms
    return cv2.waitKey(t)


def showImage(img=None, name='Imshow'):
    if img is None:
        global lastImported
        if lastImported is None:
            raise RuntimeError('Nothing has been imported')
        cv2.imshow('Last Imported', lastImported)
        return
    cv2.imshow(name, img)


def releaseAllWindows() :
    cv2.destroyAllWindows()


def chopImage(img: np.ndarray, pt1, pt2) -> np.ndarray:
    return img[pt1[1]: pt2[1], pt1[0]: pt2[0], :].copy()


def drawBox(img: np.ndarray, pt1, pt2) -> np.ndarray:
    color = config['drawing']['defaultLineColor']
    thick = config['drawing']['defaultLineThickness']
    return cv2.rectangle(img, pt1, pt2, color, thick)

def matchTemplate(img: np.ndarray, template: np.ndarray) -> np.ndarray:
    method = config['imageMatching']['method']
    imR = extractColorChannel(img, ColorName.RED)
    imG = extractColorChannel(img, ColorName.GREEN)
    imB = extractColorChannel(img, ColorName.BLUE)
    templateR = extractColorChannel(template, ColorName.RED)
    templateG = extractColorChannel(template, ColorName.GREEN)
    templateB = extractColorChannel(template, ColorName.BLUE)
    resR = cv2.matchTemplate(imR, templateR, method)
    resG = cv2.matchTemplate(imG, templateG, method)
    resB = cv2.matchTemplate(imB, templateB, method)
    res =  cv2.sqrt(resR * resR + resB * resB + resG * resG)
    res *= (255.0 / res.max())  #Normalize to 255 for imshow()
    res = np.rint(res).astype('uint8')
    return res


def matchTemplateExact(img:np.ndarray, template:np.ndarray):
    res = matchTemplate(img, template)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = min_loc
    tsize = getImageSize(template)
    center = (top_left[0] + tsize[0] // 2 ,
              top_left[1] + tsize[1] // 2)  # (x,y)
    return center, min_val

