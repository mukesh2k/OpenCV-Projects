import mediapipe as mp
import cv2


class poseDectector:
    def __init__( self,mode=False,upper_body=False,smooth=True,dection=0.5,trackcon=0.5):
        self.mode=mode
        self.upper_body=upper_body
        self.smooth=smooth
        self.dection=dection
        self.trackcon=trackcon
        self.mppose=mp.solutions.pose
        self.pose = self.mppose.Pose(self.mode,self.upper_body,self.smooth, self.dection,self.trackcon)
        self.mpdraw=mp.solutions.drawing_utils

    def findpos(self,img,draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result=self.pose.process(imgRGB)
        #print(result.pose_landmarks)
        if draw and self.result.pose_landmarks:
            self.mpdraw.draw_landmarks(img,self.result.pose_landmarks,self.mppose.POSE_CONNECTIONS)
        return img


    def getPostiton(self,img,draw=True):
        lmlist=[]
        if self.result.pose_landmarks:
            for id,lm in enumerate(self.result.pose_landmarks.landmark):
                h,w,c=img.shape
                #  print(id,lm)
                px,py=int(lm.x*w),int(lm.y*h)
                lmlist.append([id,px,py])


        return lmlist




