import cv2
import posemodule as poss
import time



cap = cv2.VideoCapture('video/Basic Running Tips _ Jogging Tips (1).mp4')
pretime = 0
hey = poss.poseDectector()
while True:
    success, img = cap.read()
    img = hey.findpos(img, True)
    lis = hey.getPostiton(img)
    if len(lis) != 0:
        print(lis[4])
        cv2.circle(img, (lis[4][1], lis[4][2]), 4, (255, 0, 255), 2)
    curtime = time.time()
    fps = 1 / (curtime - pretime)
    pretime = curtime

    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 8, 255), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)