import cv2

config = {
    "logging" : {
        "file" : 'log\\main.log',
        "path" : 'log\\'
    },

    "resource": {
        "path" : 'E:\\GirlsFrontlineAssis\\resource\\'
    },

    "snapshot": {
        "AdbPath" : 'C:\\"Program Files"\\Genymobile\\Genymotion\\tools\\adb',
        "remotePath": "/mnt/sdcard/output.png",
        "localPath" : "E:\\GirlsFrontlineAssis\\snap.png"
    },

    "drawing": {
        "defaultWindow" : "GUI",
        "defaultLineColor" : (0, 0, 255),
        "defaultLineThickness": 2
    },

    "imageMatching": {
        "method" : cv2.TM_SQDIFF
    }
}

testImage = 'test.png'