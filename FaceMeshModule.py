import cv2
import mediapipe as mp
import time

class FaceMesh():
    def __init__(self,static_image_mode=False,
               max_num_faces=1,
               min_detection_confidence=0.5,
               min_tracking_confidence=0.5):
        self.static_image_mode = static_image_mode
        self.max_num_faces = max_num_faces
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.mpdraw=mp.solutions.drawing_utils
        self.mpfm=mp.solutions.face_mesh
        self.drawspec=self.mpdraw.DrawingSpec(thickness=1,circle_radius=2)
        self.fm=self.mpfm.FaceMesh(self.static_image_mode,self.max_num_faces, self.min_detection_confidence,self.min_tracking_confidence)
        pre=0
        cur=0


    def findfacemesh(self,img,draw=True):
        rgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.result=self.fm.process(rgb)
        faces = []
        if self.result.multi_face_landmarks:
            for id1,face in enumerate(self.result.multi_face_landmarks,1):
                if draw:
                    self.mpdraw.draw_landmarks(img,face,self.mpfm.FACE_CONNECTIONS,self.drawspec,self.drawspec)
                face1=[]
                for id,lm in enumerate(face.landmark):
                    ih,iw,ic=img.shape
                    x,y=int(lm.x*iw),int(lm.y*ih)
                    face1.append([id,x,y])
                cv2.putText(img,str(id1), (x, y), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
                faces.append(face1)
        return img,faces


def main():
    cap = cv2.VideoCapture("video/10 English Expressions in 2 Minutes.mp4")
    pre=0
    FaceM=FaceMesh()
    while True:
        success, img = cap.read()
        img,out = FaceM.findfacemesh(img)
        print (len(out))
        cur = time.time()
        t = cur - pre
        if t == 0:
            fps = 1
        else:
            fps = 1 / t
        pre = cur
        cv2.putText(img, f'fps:{str(int(fps))}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()