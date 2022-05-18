import pickle
import cv2
import cvzone
import numpy as np
import datetime

cap = cv2.VideoCapture(
    '/Users/maksymbardakh/Documents/Uni/Subjects/3rdSemester/Data Analysis/KRpark/Data/parking_video.mp4')

with open('LotsPos', 'rb') as f:
    parkPos = pickle.load(f)
# with open('LotsPos', 'rb') as n:
#     parkPosOc = pickle.load(n)
tm = datetime.datetime.now()
width, height = 24, 13


# width, height = 106, 46


def checkParkingSpace(srcProcessed):
    global tm
    spaceCounter = 0

    for pos in parkPos:

        x, y = pos
        w, h = width, height
        scrCrop = srcProcessed[y:y + h, x:x + w]
        tm = datetime.datetime.now()
        count = cv2.countNonZero(scrCrop)

        if count < 56:  # 900
            color = (0, 255, 0)
            thickness = 1
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 1

        cv2.rectangle(src, (x, y), (x + w, y + h), color, thickness)
        cvzone.putTextRect(src, str(count), (x, y + height - 3), scale=0.75,
                           thickness=1, offset=0, colorR=color)

    cvzone.putTextRect(src, f'Free: {spaceCounter} OF {len(parkPos)} ', (30, 42), scale=3,
                       thickness=4, offset=20, colorR=(0, 200, 0))
    cvzone.putTextRect(src, f'Time:{tm}', (30, 90), scale=1,
                       thickness=1, offset=20, colorR=(0, 200, 0))

    print((str(count)))


while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, src = cap.read()
    srcGray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    srcBlur = cv2.GaussianBlur(srcGray, (5, 5), 0)
    srcThreshold = cv2.adaptiveThreshold(srcBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    srcMedian = cv2.medianBlur(srcThreshold, 5)

    kernel = np.ones((3, 3), np.uint8)
    srcErosion = cv2.erode(srcMedian, kernel, iterations=1)
    srcDilate = cv2.dilate(srcErosion, kernel, iterations=4)

    checkParkingSpace(srcDilate)
    cv2.imshow("Image", src)
    # cv2.imshow("srcGray", srcGray)
    # cv2.imshow("srcBlur", srcBlur)
    # cv2.imshow("srcThres", srcThreshold)
    # cv2.imshow("srcMedian", srcMedian)
    # cv2.imshow("Erosion", srcErosion)
    # cv2.imshow("srcDilate", srcDilate)
    cv2.waitKey(10)
