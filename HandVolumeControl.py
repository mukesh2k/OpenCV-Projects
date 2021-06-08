import cv2
import numpy as np
import time
import handTrackingModule as ht
import math

widhc,hc=640,480
cap=cv2.VideoCapture(0)
cap.set(3,widhc)
cap.set(4,hc)
cur,pre=0,0
h=ht.handDetector(detectioncofi=0.75)


from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volumerange=volume.GetVolumeRange()

minV=volumerange[0]
maxV=volumerange[1]







while True:

    success, img=cap.read()
    h.findHand(img)
    lists=h.findposition(img)
    x1,y1,y2,x2=0,0,0,0
    if len(lists)!=0:
        #print (lists[2])
        x1,y1=lists[4][1],lists[4][2]
        x2,y2=lists[8][1],lists[8][2]
    cv2.circle(img,(x1,y1),15,(255,0,0),3)
    cv2.circle(img,(x2, y2), 15, (255, 0, 0), 3)
    cv2.circle(img, ((x2 + x1)//2,(y2 + y1)//2), 15, (255, 0, 0), 3)
    cv2.line(img,(x1,y1),(x2,y2),(255,111,255),3)
    length=math.hypot(x2-x1,y2-y1)
    t=np.interp(length,[50,200],[minV,maxV])
    if length!=0:
        volume.SetMasterVolumeLevel(t, None)
    print(length)
    if length > 50:
        cv2.circle(img, ((x2 + x1)//2, (y2 + y1)//2), 15, (255, 0, 255), 3)
    cur=time.time()
    fps=1/(cur-pre)
    pre=cur
    cv2.putText(img,f'FPS:{str(int(fps))}',(20,70),cv2.FONT_HERSHEY_PLAIN,1,(255,0,255),2)
    cv2.imshow("Img",img)

    cv2.waitKey(1)