import win32gui
import win32ui
import win32api
import logging
import os

from config import *

from ctypes import windll
from PIL import Image


class SnapShooter(object):

    def __init__(self, name:str, scale=1.25):
        self.scale = scale

        logger = logging.getLogger(__name__)
        logger.info('id = %x, Opening Window of name :"%s"' % (id(self), name))

        self.__hwnd = win32gui.FindWindow(None, name)

        if self.__hwnd == 0:
            errmsg = 'Window hwnd not acquired, possible window not found'
            logger.error(errmsg)
            raise RuntimeError(errmsg)

        logger.debug("Window hWnd = %d" % self.__hwnd)

        # Change the line below depending on whether you want the whole window
        # or just the client area.
        # left, top, right, bot = win32gui.GetClientRect(self.__hwnd)
        left, top, right, bot = win32gui.GetWindowRect(self.__hwnd)

        # err = win32api.GetLastError()

        logger.debug("left, top, right, bot = %d, %d, %d, %d"
                     % (left, top, right, bot))

        self.__w = int(self.scale * (right - left))
        self.__h = int(self.scale * (bot - top))

        logger.debug("width = %d, height = %d" % (self.__w, self.__h))

        self.__hwndDC = win32gui.GetWindowDC(self.__hwnd)
        self.__mfcDC = win32ui.CreateDCFromHandle(self.__hwndDC)
        self.__saveDC = self.__mfcDC.CreateCompatibleDC()
        pass

    def __del__(self):
        logger = logging.getLogger(__name__)
        logger.info("Cleaning up SnapShooter, id = %x" % id(self))
        try:
            self.__saveDC.DeleteDC()
            self.__mfcDC.DeleteDC()
            win32gui.ReleaseDC(self.__hwnd, self.__hwndDC)
        finally:
            pass

    def screenShot(self):
        logger = logging.getLogger(__name__)
        logger.info("Taking snapshot")

        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(self.__mfcDC, self.__w, self.__h)

        self.__saveDC.SelectObject(saveBitMap)

        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(self.__mfcDC, self.__w, self.__h)

        self.__saveDC.SelectObject(saveBitMap)

        # Change the line below depending on whether you want the whole window
        # or just the client area.
        # result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
        result = windll.user32.PrintWindow(self.__hwnd, self.__saveDC.GetSafeHdc(), 0)

        if result == 1:
            logger.info('Snapshot taken successfully')
        else:
            err = win32api.GetLastError()
            msg = win32api.FormatMessage(err)
            logger.error("Cannot take snapshot, "
                         "Error %d: %s" % (err, msg))
            raise RuntimeError('Cannot Take Snapshot of Window')

        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)

        im = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)

        win32gui.DeleteObject(saveBitMap.GetHandle())

        return im


class SnapFetcher(object):

    def __init__(self, *args, **kwargs):
        self.__adb = config['snapshot']['AdbPath']
        self.__remoteLocation = config['snapshot']['remotePath']
        self.__localDest = config['snapshot']['localPath']
        logger = logging.getLogger(__name__)
        logger.info('Using ADB as screen fetcher')

    def screenShot(self):
        logger = logging.getLogger(__name__)
        logger.info('Taking snapshot...')
        command = (self.__adb + ' ' +
                   'shell screencap -p "%s"' % self.__remoteLocation +
                   ' && ' + self.__adb + ' ' +
                   'pull "%s" "%s"' % (self.__remoteLocation, self.__localDest) +
                   ' && ' + self.__adb + ' ' +
                   'shell rm "%s"' % self.__remoteLocation)
        logger.debug('Command Executed: %s' % command)
        ret = os.system(command)
        if ret == 0:
            logger.info('Snapshot Fetched successed')
        else:
            logger.error('Cannot Fetch Snapshot, ret = %d' %(ret))
            raise RuntimeError('Cannot Fetch Snapshot')


def simulateTouch(x, y):
    adb = config['snapshot']['AdbPath']
    logger = logging.getLogger(__name__)
    logger.info('Sending Touchevent Through ADB (%d, %d)' % (x, y))
    command = (adb + ' ' +
               'shell input tap %d %d"' % (x, y))
    logger.debug('Command Executed: %s' % command)
    ret = os.system(command)
    if ret == 0:
        logger.debug('command sent')
    else:
        logger.error('Fail to send command' % (ret))