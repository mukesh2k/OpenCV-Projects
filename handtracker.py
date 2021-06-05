import cv2
import mediapipe as mp
import time
import handTrackingModule as han


def main():
    pTime = 0
    handers=han.handDetector()
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