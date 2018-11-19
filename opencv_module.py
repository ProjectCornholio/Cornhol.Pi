import signal
import numpy as np
import cv2

class Camera():
    def __init__(self):
        print "Initializing Camera..."
        self.__cap = cv2.VideoCapture(0)
        self.__red_count = 0
        self.__prev_red = 5
        self.__blue_count = 0
        self.__prev_blue = 5

        self.__red_lower = np.array([135, 117, 42], np.uint8)
        self.__red_upper = np.array([180, 255, 255], np.uint8)
        self.__blue_lower = np.array([91, 100, 72], np.uint8)
        self.__blue_upper = np.array([118, 255, 255], np.uint8)
        self.__kernal = np.ones((5,5), "uint8")
        self.__min_bag_area = 700
        print "Done"

    def read(self, gui=False):
        # Capture frame-by-frame
        red_count = 0
        blue_count = 0
        ret, frame = self.__cap.read()
        
        mask = np.zeros((480, 640), dtype=np.uint8)
        roi = [(90, 480),(190, 10),(435, 10), (525, 480)]
        cv2.fillConvexPoly(mask, np.array(roi), 255)
        frame = cv2.bitwise_and(frame, frame, mask=mask)
        #frame = frame[0:720, 85:525]

        # set color values in hsv spectrum and dilate
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        red = cv2.inRange(hsv, self.__red_lower, self.__red_upper)
        blue = cv2.inRange(hsv, self.__blue_lower, self.__blue_upper)
        red_dilate = cv2.dilate(red, self.__kernal)
        blue_dilate = cv2.dilate(blue, self.__kernal)

        contours, hierarchy = cv2.findContours(red_dilate,
                                               cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(frame, contours, -1, (0,0,255), 2)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > self.__min_bag_area):
               red_count += 1

        contours, hierarchy = cv2.findContours(blue_dilate,
                                               cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(frame, contours, -1, (255,0,0), 2)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > self.__min_bag_area):
                blue_count += 1

        if gui:
            cv2.imshow("Color Tracking", frame)
            cv2.waitKey(10)

        return red_count, blue_count

    def close(self):
        self.__cap.release()
        cv2.destroyAllWindows()

def main():
    cap = cv2.VideoCapture(0)
    red_count = 0
    prev_red = 5
    blue_count = 0
    prev_blue = 5

    red_lower = np.array([135, 64, 43], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)
    blue_lower = np.array([91, 74, 65], np.uint8)
    blue_upper = np.array([124, 255, 255], np.uint8)
    kernal = np.ones((5,5), "uint8")
    min_bag_area = 700

    while(True):
        # Capture frame-by-frame
        red_count = 0
        blue_count = 0
        ret, frame = cap.read()
        frame = frame[0:720, 85:525]

        # set color values in hsv spectrum and dilate
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        red = cv2.inRange(hsv, red_lower, red_upper)
        blue = cv2.inRange(hsv, blue_lower, blue_upper)
        red_dilate = cv2.dilate(red, kernal)
        blue_dilate = cv2.dilate(blue, kernal)

        res = cv2.bitwise_and(frame, frame, mask=red)
        res1 = cv2.bitwise_and(frame, frame, mask=blue)

        # NOTE: rename contours to bags? not actually just bags, it's all countours being found
        contours, hierarchy = cv2.findContours(red_dilate,
                                               cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(frame, contours, -1, (0,0,255), 2)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > min_bag_area):
               red_count += 1

        contours, hierarchy = cv2.findContours(blue_dilate,
                                               cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(frame, contours, -1, (255,0,0), 2)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > min_bag_area):
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

def sig_handler(signal, frame):
    global RUN
    RUN = False

if __name__ == "__main__":
    global RUN
    RUN = True
    signal.signal(signal.SIGINT, sig_handler)
    
    cam = Camera()
    red_cnt = 0
    blue_cnt = 0
    prev_red = red_cnt
    prev_blue = blue_cnt

    while RUN:
        red_cnt, blue_cnt = cam.read(gui=True)
        if prev_red != red_cnt or prev_blue != blue_cnt:
            print "RED COUNT: %s\t\nBLUE COUNT:%s\t\n" % (str(red_cnt), str(blue_cnt))
            prev_red = red_cnt
            prev_blue = blue_cnt
    cam.close()
    #main()

