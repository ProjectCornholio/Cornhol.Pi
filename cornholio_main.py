#!/usr/bin/python

import sys
import time
import signal
import threading

# import bluetooth.ble as bt
# import bluetooth as bt

import opencv_MOCK as camera
import color_sensor_MOCK as color_sensor

# Globals
RUN = True
NUM_THREADS = 0

BOARD_RED = 0
BOARD_BLUE = 0
HOLE_RED = 0
HOLE_BLUE = 0

# SRV_SOCK = bt.BluetoothSocket(bt.RFCOMM)
# SRV_SOCK.bind(("", bt.PORT_ANY))
# SRV_SOCK.listen(1)
# CLI_SOCK, CLI_INFO = SRV_SOCK.accept()

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

def rx_bt(buffsize):
    # global CLI_SOCK
    # print CLI_SOCK.recv(buffsize)
    print buffsize

def tx_bt(msg):
    # global CLI_SOCK
    # CLI_SOCK.send(msg)
    print msg

def main():
    global RUN

    last_send = 0
    while RUN:
        HOLE_RED, HOLE_BLUE = color_sensor.read()

        # read camera and send to phone every sec
        curr_time = time.time()
        if curr_time - last_send > 1:
            BOARD_RED, BOARD_BLUE = camera.read()
            msg = "Board:\tRED: %s\n\tBLUE: %s\n" % (BOARD_RED, BOARD_RED)
            msg += "Hole:\tRED: %s\n\tBLUE: %s\n" % (HOLE_RED, HOLE_BLUE)
            tx_bt(msg)
            last_send = curr_time

    print "We out!"

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    # thread.start_new_thread(test_thread, ())
    # my_thread = threading.Thread(target=test_thread, args=(), kwargs={})
    # my_thread.start()
    main()
    while threading.active_count() > 1:
        # main will count as a thread, so we're looking for more than 1
        # print "active threads:", threading.active_count()
        pass
