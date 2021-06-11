import cv2
import numpy as np
import time
import os
import handTrackingModule as hm

pre,cur=0,0
paths="designs"
mylist=os.listdir(paths)
cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
overlay =[]
for impath in mylist:
    imgg=cv2.imread(f'{paths}/{impath}')
    overlay.append(imgg)
print(len(overlay))
head=overlay[0]
drawcolor=(255,0,255)
thick=15
xp=0
yp=0
he=hm.handDetector(detectioncofi=0.7)
imcanva=np.zeros((720,1280,3),np.uint8)
while True:
    success,img=cap.read()
    img=cv2.flip(img,1)
    landlist = he.findposition(img, draw=False)
    img=he.findHand(img)

    #print(landlist)
    if len(landlist) !=0:

        #print(landlist)
        x1,y1=landlist[8][1],landlist[8][2]
        x2,y2=landlist[12][1],landlist[12][2]
        state=he.opencheck()
        if state[1] and state[2]:
            xp = 0
            yp = 0
            print("select")
            cv2.rectangle(img,(x1,y1-25),(x2,y2+25),(255,0,255),cv2.FILLED)
            if y1<125:
                if 250<x1<350:
                    head=overlay[2]
                    thick = 15
                    drawcolor=(255,0,255)
                elif 350<x1<650:
                    head=overlay[1]
                    thick=15
                    drawcolor=(255, 0, 0)
                elif 800<x1<1250:
                    head=overlay[0]
                    thick=30
                    drawcolor = (0, 0, 0)
        elif state[1] and state[2]==False:
            cv2.circle(img,(x1,y1),15,drawcolor,cv2.FILLED)
            if xp==0 and yp==0:
                xp,yp=x1,y1
            cv2.line(img,(xp,yp),(x1,y1),drawcolor,thick)
            cv2.line(imcanva, (xp, yp), (x1, y1), drawcolor, thick)
            xp,yp=x1,y1
            print ("unselect")

    cur=time.time()
    fps=1/(cur-pre)
    pre=cur
    imgray=cv2.cvtColor(imcanva,cv2.COLOR_BGR2GRAY)
    _,imgInv=cv2.threshold(imgray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv=cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img=cv2.bitwise_and(img,imgInv)
    img=cv2.bitwise_or(img,imcanva)
    #img=cv2.addWeighted(img,0.5,imcanva,0.5,0)
    img[0:125, 0:1280] = head
    cv2.imshow("Webcam",img)
    # cv2.imshow("canvas", imcanva)
    cv2.waitKey(1)