import cv2
import pickle

# width, height = 106, 46
width, height = 24, 13
try:
    with open('LotsPos', 'rb') as f:
        parkPos = pickle.load(f)
except:
    parkPos = []


def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        parkPos.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(parkPos):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                parkPos.pop(i)
    with open('LotsPos', 'wb') as f:
        pickle.dump(parkPos, f)


while True:
    # cv2.rectangle(img,(50,192),(157,240),(255,0,255),2)
    img = cv2.imread('/Users/maksymbardakh/Documents/Uni/Subjects/3rdSemester/Data Analysis/KRpark/Data/videoPark.png')
    for pos in parkPos:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 255, 0), 1)
    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)
    cv2.waitKey(1)
