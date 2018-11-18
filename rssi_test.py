#!/usr/bin/python

import os.path
import signal
import time
import subprocess as sp
import numpy as np
from openpyxl import Workbook
from openpyxl.chart import (ScatterChart,
                            Reference,
                            Series)

def write_excel(data, fname):
    # write data to excel spreadsheet
    wb = Workbook()
    ws = wb.active
    for row in data:
        ws.append(row)

    # create
    chart = ScatterChart()
    chart.title = "RSSI v. Distance (ft)"
    chart.style = 1
    chart.x_axis.title = "Distance"
    chart.y_axis.title = "RSSI"

    x_values = Reference(ws, min_col=1, min_row=1, max_row=len(data))
    y_values = Reference(ws, min_col=2, min_row=1, max_row=len(data))
    series = Series(y_values, x_values, title_from_data=True)
    chart.series.append(series)
    ws.add_chart(chart, "D2")

    wb.save(fname)
    print "%s saved!" % (fname)

def sig_handler(sig, frame):
    global RUN
    RUN = False

def get_avg_rssi(duration=0):
    pi_mac = "B4:F1:DA:6B:43:E4"
    cmd = "hcitool rssi %s" % (pi_mac)

    if duration != 0:
        rssi_values = []
        start = time.time()
        while time.time() - start < duration:
            hci_output = sp.check_output(cmd.split()).strip()
            rssi = int(hci_output.split()[3])
            rssi_values.append(rssi)
        return float(format(np.mean(rssi_values), ".2f"))

    else:
        hci_output = sp.check_output(cmd.split()).strip()
        rssi = int(hci_output.split()[3])
        return float(format(rssi, ".2f"))

def rssi_test():
    global RUN
    RUN = True
    data = []
    while RUN:
        try:
            print "Distance:",
            distance = int(raw_input())
            data.append([distance , get_avg_rssi(1)])
        except ValueError:
            print "Dingus"
        except KeyboardInterrupt:
            RUN = False
            print

    fname_base = "rssi_measurements%s.xlsx"
    fname = fname_base % ("")
    i = 1
    while os.path.exists(fname):
        fname = fname_base % ("_" + str(i))
        i += 1
    write_excel(data, fname)

if __name__ == "__main__":
    rssi_test()
