import numpy as np
import cv2

cap = cv2.VideoCapture(0)
red_count = 0
prev_red = 5
blue_count = 0
prev_blue = 5

while(True):
    # Capture frame-by-frame
    red_count = 0
    blue_count = 0
    ret,frame = cap.read()

    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    red_lower = np.array([135,64,43],np.uint8)
    red_upper = np.array([180,255,255],np.uint8)

    blue_lower = np.array([91,74,71],np.uint8)
    blue_upper = np.array([124,255,255],np.uint8)

    red = cv2.inRange(hsv, red_lower, red_upper)
    blue = cv2.inRange(hsv, blue_lower, blue_upper)

    kernal = np.ones((5,5),"uint8")
    red1 = cv2.dilate(red, kernal)
    res = cv2.bitwise_and(frame, frame, mask = red)

    blue1 = cv2.dilate(blue, kernal)
    res1 = cv2.bitwise_and(frame, frame, mask = blue)

    contours,hierarchy = cv2.findContours(red1,cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
   # contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
    cv2.drawContours(frame, contours, -1, (0,0,255),2)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area>700):
           # x,y,w,h = cv2.boundingRect(contour)
           #cv2.drawContours(frame,contours,-1,(0,0,255),2)
           # cv2.putText(frame,"RED color",(x,y),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255))
           red_count += 1

    contours,hierarchy = cv2.findContours(blue1,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame, contours, -1, (255,0,0), 2)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area>700):
            #cv2.drawContours(frame,contours,-1,(255,0,0),2)
           # cv2.putText(frame,"BLUE color",(x,y),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,0,0))
            blue_count += 1

    if blue_count != prev_blue or red_count != prev_red:
        print("Red Count: " + str(red_count))
        print("Blue Count: " + str(blue_count))
        prev_red = red_count
        prev_blue = blue_count


    cv2.imshow("Color Tracking",frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break

