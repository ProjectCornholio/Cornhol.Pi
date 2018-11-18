#!/usr/bin/python

import sys
import time
import signal
import numpy
import threading

# import bluetooth.ble as bt
import bluetooth as bt

import opencv_module
import color_sensor_module

# Globals
RUN = True
NUM_THREADS = 0

BOARD_RED = 0
BOARD_BLUE = 0
HOLE_RED = 0
HOLE_BLUE = 0

class PhoneBT():
    def __init__(self, port=bt.PORT_ANY):
        print "Initializing Bluetooth connection with phone..."
        self.__srv_sock = bt.BluetoothSocket(bt.RFCOMM)
        self.__srv_sock.bind(("", port))
        self.__srv_sock.listen(1)
        '''
        self.__uuid = "aba30ef4-6074-4e27-b929-ac14e4b324a9"
        bt.advertise_service(self.__srv_sock, "Cornhol.io_1",
                             service_id = self.__uuid,
                             service_classes = [self.__uuid, bt.SERIAL_PORT_CLASS],
                             profiles = [bt.SERIAL_PORT_PROFILE]
                             )
        '''
        self.__cli_sock, self.__cli_addr = self.__srv_sock.accept()
        self.__conn_good = True
        print "Connection established!"
        pass

    def tx(self, msg):
        try:
            return self.__cli_sock.send(msg)
        except bt.btcommon.BluetoothError:
            print "Lost connection to phone. Attempting to reconnect..."
            self.reconnect()

    def rx(self, buff_size=255):
        return self.__cli_sock.recv(size)

    def reconnect(self):
        self.__cli_sock, self.__cli_addr = self.__srv_sock.accept()
        print "We back boiiiii"

    def close(self):
        print "Closing connection to phone"
        self.__srv_sock.close()
        self.__cli_sock.close()

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

def main():
    global RUN, BOARD_RED, BOARD_BLUE, HOLE_RED, HOLE_BLUE

    phone = PhoneBT()
    color_sensor = color_sensor_module.ColorSensor()
    camera = opencv_module.Camera()

    last_send = 0
    while RUN:
        BOARD_RED, BOARD_BLUE = camera.read(gui=True)
        new_red, new_blue = color_sensor.read()
        HOLE_RED += new_red
        HOLE_BLUE += new_blue

        # read camera and send to phone every sec
        curr_time = time.time()
        if curr_time - last_send > 1:
            msg = "Board:\tRED: %s\n\tBLUE: %s\n" % (BOARD_RED, BOARD_BLUE)
            msg += "Hole:\tRED: %s\n\tBLUE: %s\n" % (HOLE_RED, HOLE_BLUE)
            #phone.tx(msg)
            print msg
            last_send = curr_time

    camera.close()
    #phone.close()

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
