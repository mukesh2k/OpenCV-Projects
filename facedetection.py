import cv2
import mediapipe as mp
import time

cap=cv2.VideoCapture("video/10 English Expressions in 2 Minutes.mp4")
curt=0
pret=0
mpface=mp.solutions.face_detection
mpdraw=mp.solutions.drawing_utils
facedecte=mpface.FaceDetection(0.75)
while True:
    success, img=cap.read()
    convert=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    result=facedecte.process(convert)
    if result:
        for id,detect in enumerate(result.detections):
            print(id,detect)
            mpdraw.draw_detection(img,detect)
            bboxC=detect.location_data.relative_bounding_box
            #print(bboxC)
            ih,iw,ic=img.shape
            bbox=int(bboxC.xmin*iw),int(bboxC.ymin*ih), \
                 int(bboxC.width*iw),int(bboxC.height*ih)
            #cv2.rectangle(img,bbox,(255,0,255),2)
            cv2.putText(img, str(int(detect.score[0]*100)), (bbox[0], bbox[1]-20), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 8, 255), 1)
    curt=time.time()
    fps=(1/(curt-pret))
    pret=curt

    cv2.imshow("Image", img)
    cv2.waitKey(25)