import log
import device


def main():
    log.setLoggers()

    str = 'Genymotion for personal use - Custom Phone - 5.1.0 - API 22 - 768x1280 (1280x768, 240dpi) - 192.168.29.101'

    str2 = 'Bluestacks App Player'
    try:
        snap = device.SnapFetcher(str2)
    finally:
        pass

    snap.screenShot()
    # im.save('a.png')


main()
