import os
import time
import cv2
import handTrackingModule as ht
cap=cv2.VideoCapture(0)
wid,hei=640,480
cap.set(3,wid)
cap.set(4,hei)
cur,pre=0,0
hand=ht.handDetector()
tipid=[8,12,16,20]
state=[]
while True:
    sucess,img=cap.read()
    cur=time.time()
    fps=1/(cur-pre)
    pre=cur
    lists=hand.findposition(img)
    cv2.putText(img, f'FPS: {int(fps)}', (20, 60), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
    if len(lists)!=0:
        state.append(lists[4][1]>lists[3][1])
        for x in tipid:
            state.append(lists[x][2]<lists[x-2][2])#true open
        count = 0
        for o in state:
            if o:
                count += 1

        cv2.putText(img, f'TotalFingers Open: {count}', (20, 90), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
        cv2.putText(img, f'Thumb Open {state[0]}', (20, 120), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
        cv2.putText(img, f'ForeFinger Open {state[1]}', (20, 150), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
        cv2.putText(img, f'MiddleFinger Open {state[2]}', (20, 180), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
        cv2.putText(img, f'RingFinger Open {state[3]}', (20, 210), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
        cv2.putText(img, f'PinkyFinger Open {state[4]}', (20, 240), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
    print(state)
    img=hand.findHand(img)

    cv2.imshow("Image", img)
    state.clear()
    cv2.waitKey(2)
