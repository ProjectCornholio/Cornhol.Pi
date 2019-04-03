#!/usr/bin/python

import sys
import time
import signal
import numpy
import select
import subprocess as sp
from gpiozero import Button

# import bluetooth.ble as bt
import bluetooth as bt

import opencv_MOCK as opencv_module
import color_sensor_MOCK as color_sensor_module

# Globals
RUN = True
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
        conn_ready = select.select([self.__cli_sock], [], [], 0.1)
        if self.__conn_good and conn_ready[0]:
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

def tx_to_phone(phone):
    global RUN, BOARD_RED, BOARD_BLUE, HOLE_RED, HOLE_BLUE
    msg = "Board:\tRED: %s\n\tBLUE: %s\n" % (BOARD_RED, BOARD_BLUE)
    msg += "Hole:\tRED: %s\n\tBLUE: %s\n" % (HOLE_RED, HOLE_BLUE)
    phone.tx("%s,%s,%s,%s" % (BOARD_RED, HOLE_RED,
             BOARD_BLUE, HOLE_BLUE))
    print msg

def rx_to_phone(phone):
    global RUN, BOARD_RED, BOARD_BLUE, HOLE_RED, HOLE_BLUE
    msg = phone.rx(255)
    if msg != None:
        msg = msg.strip() 
        print msg
        if msg == "STOP": 
            RUN = False
        elif msg == "CLEAR":
            BOARD_RED = 0
            BOARD_BLUE = 0
            HOLE_RED = 0
            HOLE_BLUE = 0

def do_bt_pairing():
    sp.call(r"echo -e 'discoverable on\npairable on\nexit\n' | bluetoothctl")
    return

def signal_handler(sig, frame):
    global RUN
    RUN = False

def main(phone):
    global RUN, BOARD_RED, BOARD_BLUE, HOLE_RED, HOLE_BLUE

    color_sensor = color_sensor_module.ColorSensor()
    camera = opencv_module.Camera()
    pairing_btn = Button(24) # button connected to GPIO24
    pairing_btn.when_pressed = do_bt_pairing

    prev_time = 0
    while RUN:
        BOARD_RED, BOARD_BLUE = camera.read(gui=True)
        new_red, new_blue = color_sensor.read()
        HOLE_RED += new_red
        HOLE_BLUE += new_blue

        send_rate = .5
        curr_time = time.time()
        if curr_time - prev_time > send_rate:
            tx_to_phone(phone)
            rx_to_phone(phone)
            prev_time = time.time()

    camera.close()
    if phone.is_connected():
        phone.close()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    # thread.start_new_thread(test_thread, ())
    phone = PhoneBT()
    if phone == None:
        sys.exit()
    main(phone)
