import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__ (self,mode=False,maxHands=2,detectioncofi=0.5,trackconf=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.detectconfi=detectioncofi
        self.trackconfi=trackconf
        self.mphand=mp.solutions.hands
        self.hands=self.mphand.Hands(self.mode,self.maxHands, self.detectconfi, self.trackconfi)
        self.mpDraw=mp.solutions.drawing_utils
        self.tipid=[8,12,16,20]
        self.lisy=[]
        self.imgRGB=[]
    def findHand(self,img,draw=True):
        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results=self.hands.process(imgRGB)
       # print(self.results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for cx in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, cx, self.mphand.HAND_CONNECTIONS)
        return img



    def findposition(self,img,handNumber=0,draw=True):
        lmList=[]
        self.imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(self.imgRGB)
        if  self.results.multi_hand_landmarks:
            cx=self.results.multi_hand_landmarks[handNumber]
            for id,lm in enumerate(cx.landmark):
               # print(id,lm)
                h,w,c=img.shape
                px,py=int (lm.x*w),int (lm.y*h)
                lmList.append([id,px,py])
        self.lisy=lmList
        return lmList

    def opencheck(self):
        lists = self.lisy
        state=[]
        if len(lists) != 0:
            state.append(lists[4][1] > lists[3][1])
            for x in self.tipid:
                state.append(lists[x][2] < lists[x - 2][2])  # true open
        return state

def main():
    pTime = 0
    handers=handDetector()
    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        img=handers.findHand(img)
        lists=handers.findposition(img)
        if len(lists)!=0:
            print(lists[4])
        cur = time.time()
        fps = 1 / (cur - pTime)
        pTime = cur
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 8, 255), 2)
        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()