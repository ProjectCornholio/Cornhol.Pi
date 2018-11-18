import numpy as np
import subprocess as sp
import time

def rssi_test():
    pi_mac = "B4:F1:DA:6B:43:E4"
    cmd = "hcitool rssi %s" % (pi_mac)
    rssi_values = []
    sample_size = 20
    #for i in range(sample_size):
    start = time.time()
    sample_duration = 1
    while time.time() - start < sample_duration:
        hci_output = sp.check_output(cmd.split()).strip()
        rssi = int(hci_output.split()[3])
        rssi_values.append(rssi)
    print format(np.mean(rssi_values), ".2f")

if __name__ == "__main__":
    rssi_test()
