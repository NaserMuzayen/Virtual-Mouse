import numpy as np
import cv2 as cv


def getEvent(fingers):
    if all(fingers) == 1:
        return 'screenShot'
    elif fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 0:
        return 'rightClick'
    elif fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
        return 'leftClick'
    elif fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
        return 'scrollDown'
    elif fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
        return 'scrollUp'
    elif fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
        return 'Move'
    else:
        return 'empty'


def ScreenShot(img, time):
    image = np.array(img)
    image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
    cv.imwrite(str(time) + '.png', image)


frameR = 100
alpha = 0.5
smoothing = 4


def MoveMouse(img, x1, y1, hCam, wCam, wScreen, hScreen, plocX, plocY):
    imgCopy = img.copy()
    cv.rectangle(imgCopy, (frameR, frameR), (wCam - frameR, hCam - frameR), (50, 50, 50), -1)
    img = cv.addWeighted(imgCopy, alpha, img, 1 - alpha, 0)
    x = np.interp(x1, (frameR, wCam - frameR), (0, wScreen+20))
    y = np.interp(y1, (frameR, hCam - frameR), (0, hScreen+20))
    x = plocX + (x - plocX) / smoothing
    y = plocY + (y - plocY) / smoothing

    return img, x, y
