import cv2 as cv
import mediapipe as mp
import math


class handDetector():
    def __init__(self, mode=False, maxHands=2, model_complexity=1, detectionCon=0.5, trackCon=0.5):
        self.result = None
        self.model_complexity = model_complexity
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.model_complexity,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.lmList = []
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img, draw=False):
        rgb_image = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.result = self.hands.process(rgb_image)
        if self.result.multi_hand_landmarks:
            if draw:
                for handLms in self.result.multi_hand_landmarks:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPositions(self, img, handNo=0, draw=True):
        xList = []
        yList = []
        box = []
        self.lmList = []
        if self.result.multi_hand_landmarks:
            my_hands = self.result.multi_hand_landmarks[handNo]
            for pointId, lm in enumerate(my_hands.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                self.lmList.append([pointId, cx, cy])
                if draw:
                    cv.circle(img, (cx, cy), 5, (255, 0, 0), cv.FILLED)

            xMin, xMax = min(xList), max(xList)
            yMin, yMax = min(yList), max(yList)
            box = xMin, yMin, xMax, yMax
            if draw:
                cv.rectangle(img, (xMin - 20, yMin - 20), (xMax + 20, yMax + 20),
                             (0, 255, 0), 2)

        return self.lmList, box

    def fingersUp(self):
        fingers = []

        # Thumb > for lift hand and < for right hand
        if self.lmList[0][1] > self.lmList[2][1]:
            if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        else:
            if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        # Fingers
        for top in range(1, 5):
            if self.lmList[self.tipIds[top]][2] < self.lmList[self.tipIds[top] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

    def findDistance(self, p1, p2, img):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        length = math.hypot(x2 - x1, y2 - y1)

        return length
