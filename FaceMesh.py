import cv2
import mediapipe as mp
import time

cap=cv2.VideoCapture("video/10 English Expressions in 2 Minutes.mp4")
mpdraw=mp.solutions.drawing_utils
mpfm=mp.solutions.face_mesh
drawspec=mpdraw.DrawingSpec(thickness=1,circle_radius=2)
fm=mpfm.FaceMesh(max_num_faces=2)
pre=0
cur=0
while True:
    success,img=cap.read()
    rgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    result=fm.process(rgb)
    if result.multi_face_landmarks:
        for face in result.multi_face_landmarks:
            mpdraw.draw_landmarks(img,face,mpfm.FACE_CONNECTIONS,drawspec,drawspec)
            for id,lm in enumerate(face.landmark):
                ih,iw,ic=img.shape
                x,y=int(lm.x*iw),int(lm.y*ih)
                print(id,x,y)
    cur=time.time()
    t=cur-pre
    fps=0
    if t==0:
        fps=1
    else:
        fps=1/t
    pre=cur
    cv2.putText(img,f'fps:{str(int(fps))}',(20,70),cv2.FONT_HERSHEY_PLAIN,2,(255,0,255),2)
    cv2.imshow("Image", img)
    cv2.waitKey(1)