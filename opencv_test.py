import numpy as np
import cv2

cap = cv2.VideoCapture(0)
red_count = 0
prev_red = 5
blue_count = 0
prev_blue = 5

def main():
    global cap, red_count, prev_red, blue_count, prev_blue

    while(True):
        # Capture frame-by-frame
        red_count = 0
        blue_count = 0
        ret,frame = cap.read()
        frame = frame[0:720, 85:525] #NOTE: does this change?

        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

        # NOTE: do these red/blue values ever change?
        # set red min/max color values
        red_lower = np.array([135, 64, 43], np.uint8)
        red_upper = np.array([180, 255, 255], np.uint8)
        red = cv2.inRange(hsv, red_lower, red_upper)

        # set blue min/max color values
        blue_lower = np.array([91, 74, 65], np.uint8)
        blue_upper = np.array([124, 255, 255], np.uint8)
        blue = cv2.inRange(hsv, blue_lower, blue_upper)

        # NOTE: does kernal or red1/blue1 or res/res1 ever change?
        kernal = np.ones((5,5), "uint8")
        red1 = cv2.dilate(red, kernal)
        res = cv2.bitwise_and(frame, frame, mask = red)

        blue1 = cv2.dilate(blue, kernal)
        res1 = cv2.bitwise_and(frame, frame, mask = blue)

        # NOTE: rename contours to bags?
        contours, hierarchy = cv2.findContours(red1,
                                               cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_NONE)
       # contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
        cv2.drawContours(frame, contours, -1, (0,0,255), 2)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            # TODO: these magic numbers should be variablized
            # something like MIN_BAG_AREA
            if(area > 700):
               # x,y,w,h = cv2.boundingRect(contour)
               # cv2.drawContours(frame,contours,-1,(0,0,255),2)
               # cv2.putText(frame,"RED color",(x,y),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255))
               red_count += 1

        contours, hierarchy = cv2.findContours(blue1,
                                               cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(frame, contours, -1, (255,0,0), 2)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > 700):
                #cv2.drawContours(frame,contours,-1,(255,0,0),2)
               # cv2.putText(frame,"BLUE color",(x,y),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,0,0))
                blue_count += 1

        # display stuff
        if blue_count != prev_blue or red_count != prev_red:
            print("Red Count: " + str(red_count))
            print("Blue Count: " + str(blue_count))
            prev_red = red_count
            prev_blue = blue_count

        # GUI window
        cv2.imshow("Color Tracking",frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break

if __name__ == "__main__":
    main()
