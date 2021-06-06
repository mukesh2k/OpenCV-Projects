import cv2
import mediapipe as mp
import time

class FaceModule():
    def __init__(self,minDectcor=0.5):
        self.minDectconf=minDectcor
        self.mpface = mp.solutions.face_detection
        self.mpdraw = mp.solutions.drawing_utils
        self.facedecte = self.mpface.FaceDetection(self.minDectconf)


    def findface(self,img,draw=True):
        convert = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.facedecte = self.mpface.FaceDetection(0.75)
        self.result = self.facedecte.process(convert)
        bboxs=[]
        if self.result:
            for id, detect in enumerate(self.result.detections):
                #print(id, detect)
                self.mpdraw.draw_detection(img, detect)
                bboxC = detect.location_data.relative_bounding_box
                # print(bboxC)
                ih, iw, ic = img.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                       int(bboxC.width * iw), int(bboxC.height * ih)
                bboxs.append([id,bbox,detect.score])
                #
                if draw:
                    cv2.putText(img, str(int(detect.score[0] * 100)), (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_TRIPLEX, 1,
                            (255, 8, 255), 1)


        return img,bboxs


    def fancyDraw(self,img,bbox,thick=10):
        x,y,w,h=bbox
        x1,y1=x*w,y*h
        cv2.rectangle(img, bbox, (255, 0, 255), 2)
        cv2.line(img,(x,y),(x+l,y),(255,0,255),thick)
        return img

def main():
    cap = cv2.VideoCapture("video/10 English Expressions in 2 Minutes.mp4")
    curt = 0
    pret = 0
    D=FaceModule()

    while True:
        success, img = cap.read()
        img,bbox = D.findface(img)
        print(bbox)
        curt = time.time()
        fps = (1 / (curt - pret))
        cv2.putText(img,str(int(fps)),(20,70),cv2.FONT_HERSHEY_PLAIN,2,(255,0,255),2)
        pret = curt
        cv2.imshow("Image", img)
        cv2.waitKey(20)








if __name__ == "__main__":
    main()