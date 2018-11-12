import sys
import time
import signal
import thread

#import bluetooth.ble as bt
import bluetooth as bt

import opencv_mod as camera
import light_sensor_mod as light_sensor

RUN = True
NUM_THREADS = 0

def test_thread():
    global NUM_THREADS
    NUM_THREADS += 1
    while RUN:
        print "thread running"
        time.sleep(1)
    print "We out too!"
    NUM_THREADS -= 1

def signal_handler(sig, frame):
    global RUN
    RUN = False

def tx_ble(msg):
    print msg

def main():
    global RUN

    last_send = 0
    while RUN:
        light_sensor.read()

        # read camera and send to phone every sec
        curr_time = time.time()
        if curr_time - last_send > 1:
            print "camera: ", camera.read()
            tx_ble("sent to phone")
            last_send = curr_time
        
    print "We out!"

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    thread.start_new_thread(test_thread, ())
    main()
    while NUM_THREADS != 0:
        pass
