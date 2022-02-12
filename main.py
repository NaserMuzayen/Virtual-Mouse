import cv2 as cv
from Mouse import getEvent, ScreenShot, MoveMouse
import HandTrackingModule as ht
import pyautogui as auto
import time

pTime = 0
wCam, hCam = 650, 490
screenShotCounter = 0
locX, locY = 0, 0
hand = ht.handDetector()
cap = cv.VideoCapture(0)
print(cap)
cap.set(3, wCam)
cap.set(4, hCam)
bg = cv.bgsegm.createBackgroundSubtractorMOG()
wScreen, hScreen = auto.size()
while True:
    success, img = cap.read()
    cTime = time.time()
    # fps = 1 / (cTime - pTime)
    # pTime = cTime
    img = cv.flip(img, 1)
    img = hand.findHands(img, draw=True)
    positions, box = hand.findPositions(img)
    if len(positions) != 0:
        # index finger
        x1, y1 = positions[8][1:]
        # middle finger
        x2, y2 = positions[12][1:]
        # distance between index and middle
        length = hand.findDistance(8, 12, img)
        # print(length)
        # check for up finger        length = hand.findDistance(8, 12, img)
        fingers = hand.fingersUp()
        # print(fingers)
        eventType = getEvent(fingers)
        if eventType == 'screenShot':
            if screenShotCounter < 20:
                screenShotCounter += 1
            else:
                screenshot = auto.screenshot()
                ScreenShot(screenshot, cTime)
                screenShotCounter = 0
                auto.alert(text='Screenshot', title='Screenshot', timeout=1000)
        else:
            screenShotCounter = 0
            if eventType == 'scrollUp':
                auto.scroll(100)
            elif eventType == 'scrollDown':
                auto.scroll(-100)
            elif eventType == 'Move':
                img, x, y = MoveMouse(img, x1, y1, hCam, wCam, wScreen, hScreen, locX, locY)
                auto.moveTo(x, y)
                locX, locY = x, y
            elif eventType == 'leftClick' and length < 40:
                auto.click()
            elif eventType == 'rightClick' and length < 40:
                auto.rightClick()

    # cv.putText(img, 'fps : ' + str(int(fps)), (10, 70), cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 3)
    cv.imshow('image', img)
    key = cv.waitKey(2)
    if key == ord('q') or key == ord('Q'):
        break
cv.destroyAllWindows()
cap.release()
