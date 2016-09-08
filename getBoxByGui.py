from image import *
import cv2
import numpy as np

getBoxByGui_pt1 = (0, 0)
getBoxByGui_pt2 = (0, 0)
getBoxByGui_state = 0
# 0:no pt selected, 1: 1 pt with moving rect. 2: fully selected
getBoxByGui_canvas = None


def getBoxByGui_OnMouse(event, x, y, flags, param : np.ndarray):
    global getBoxByGui_canvas
    global getBoxByGui_pt1
    global getBoxByGui_pt2
    global getBoxByGui_state
    if event == cv2.EVENT_LBUTTONDBLCLK:
        if getBoxByGui_state == 0:
            getBoxByGui_state += 1
            getBoxByGui_pt1 = (x, y)
            return
        if getBoxByGui_state == 1:
            getBoxByGui_state += 1
            getBoxByGui_pt2 = (x, y)
            return
        if getBoxByGui_state == 2:
            getBoxByGui_state = 0
            return
    if event == cv2.EVENT_MOUSEMOVE:
        if getBoxByGui_state == 0:
            getBoxByGui_canvas = param.copy()
            return
        if getBoxByGui_state == 1:
            getBoxByGui_canvas = param.copy()
            getBoxByGui_canvas = drawBox(getBoxByGui_canvas,
                                         getBoxByGui_pt1, (x, y))
            return
        if getBoxByGui_state == 2:
            getBoxByGui_canvas = param.copy()
            getBoxByGui_canvas = drawBox(getBoxByGui_canvas,
                                         getBoxByGui_pt1,
                                         getBoxByGui_pt2)
            return


def getBoxByGui(img: np.ndarray):
    windowName = config['drawing']['defaultWindow']
    cv2.namedWindow(windowName)
    cv2.setMouseCallback(windowName, getBoxByGui_OnMouse, img)
    global getBoxByGui_state
    global getBoxByGui_canvas
    global getBoxByGui_pt1
    global getBoxByGui_pt2
    getBoxByGui_state = 0  # No point selected
    getBoxByGui_canvas = img.copy()
    while True:
        cv2.imshow(windowName, getBoxByGui_canvas)
        if cv2.waitKey(20) != -1:
            break
    cv2.destroyWindow(windowName)
    if getBoxByGui_state == 2:  # All points selected
        return getBoxByGui_pt1, getBoxByGui_pt2
    else:
        return None