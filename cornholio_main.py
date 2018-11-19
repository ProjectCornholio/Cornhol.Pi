#!/usr/bin/python

import sys
import time
import signal
import numpy
import threading

# import bluetooth.ble as bt
import bluetooth as bt

import opencv_MOCK as opencv_module
import color_sensor_MOCK as color_sensor_module

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
        try:
            self.__cli_sock, self.__cli_addr = self.__srv_sock.accept()
        except bt.btcommon.BluetoothError:
            print "System Err: Exiting program before establishing a connection"
            self.__srv_sock.close()
        else:
            self.__conn_good = True
            print "Connection established!"

    def tx(self, msg):
        try:
            return self.__cli_sock.send(msg)
        except bt.btcommon.BluetoothError:
            print "Lost connection to phone. Attempting to reconnect..."
            self.__conn_good = False
            self.reconnect()

    def rx(self, buff_size=255):
        if self.__conn_good:
            try:
                return self.__cli_sock.recv(buff_size)
            except bt.btcommon.BluetoothError:
                pass


    def reconnect(self):
        try:
            self.__cli_sock, self.__cli_addr = self.__srv_sock.accept()
        except bt.btcommon.BluetoothError:
            print "System Err: Exiting program"
            self.close()
            return

        self.__conn_good = True
        print "We back boiiiii"

    def is_connected(self):
        return self.__conn_good

    def close(self):
        print "Closing connection to phone"
        self.__srv_sock.close()
        self.__cli_sock.close()

def tx_thread(phone, send_rate=1):
    global NUM_THREADS, RUN, \
           BOARD_RED, BOARD_BLUE, \
           HOLE_RED, HOLE_BLUE

    NUM_THREADS += 1
    prev_time = 0
    while RUN:
        curr_time = time.time()
        if curr_time - prev_time > send_rate:
            msg = "Board:\tRED: %s\n\tBLUE: %s\n" % (BOARD_RED, BOARD_BLUE)
            msg += "Hole:\tRED: %s\n\tBLUE: %s\n" % (HOLE_RED, HOLE_BLUE)
            phone.tx(msg)
            print msg
            prev_time = time.time()
    NUM_THREADS -= 1

def rx_thread(phone):
    global NUM_THREADS, RUN, \
           BOARD_RED, BOARD_BLUE, \
           HOLE_RED, HOLE_BLUE

    NUM_THREADS += 1
    while RUN:
        try:
            msg = phone.rx(255).strip()
            print msg
            if msg == "stop":
                RUN = False
            elif msg == "clear":
                BOARD_RED = 0
                BOARD_BLUE = 0
                HOLE_RED = 0
                HOLE_BLUE = 0

        except AttributeError:
            pass
    NUM_THREADS -= 1

def signal_handler(sig, frame):
    global RUN
    RUN = False

def main(phone):
    global RUN, BOARD_RED, BOARD_BLUE, HOLE_RED, HOLE_BLUE

    color_sensor = color_sensor_module.ColorSensor()
    camera = opencv_module.Camera()

    last_send = 0
    while RUN:
        BOARD_RED, BOARD_BLUE = camera.read(gui=True)
        new_red, new_blue = color_sensor.read()
        HOLE_RED += new_red
        HOLE_BLUE += new_blue

    camera.close()
    if phone.is_connected():
        phone.close()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    # thread.start_new_thread(test_thread, ())
    phone = PhoneBT()
    if phone == None:
        sys.exit()
    my_tx_thread = threading.Thread(target=tx_thread, args=(phone,), kwargs={})
    my_rx_thread = threading.Thread(target=rx_thread, args=(phone,), kwargs={})
    my_tx_thread.start()
    my_rx_thread.start()
    main(phone)
    while threading.active_count() > 1:
        # main will count as a thread, so we're looking for more than 1
        # print "active threads:", threading.active_count()
        pass
