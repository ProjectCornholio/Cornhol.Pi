import smbus
import time

bus = smbus.SMBus(1)
bus.write_byte(0x29,0x80|0x12)
ver = bus.read_byte(0x29)
print hex(ver)

def read():
    # read register from color sensor
    data = bus.read_i2c_block_data(0x29, 0)
    clear = data[1] << 8 | data[0]
    red = data[3] << 8 | data[2]
    green = data[5] << 8 | data[4]
    blue = data[7] << 8 | data[6]

    # detected red bag
    if (red - prev_red) >= (blue - prev_blue) \
      and (red - prev_red) > 1000 \
      and count > 1:
        print "red bag detected!\n"
        #time.sleep(0.15)

    # detected blue bag
    elif (blue - prev_blue) >= 800 \
      and (blue - prev_blue) > (red - prev_red) \
      and count > 0:
        print "blue bag detected!\n"
        #time.sleep(0.15)

    #crgb = "c: %s, R: %s, G: %s, B: %s\n" % (clear, red, green, blue)
    #print crgb
    prev_red = red
    prev_blue = blue
    count += 1
    #time.sleep(1)

def main():
    global bus, ver

    if ver == 0x44:
        print "device found!/n"
        bus.write_byte(0x29, 0x80|0x00)
        bus.write_byte(0x29, 0x01|0x02)
        bus.write_byte(0x29, 0x80|0x14)
        prev_red = 0
        prev_blue = 0
        count = 0
        data = bus.read_i2c_block_data(0x29, 0)

        while True:
            read()

    else:
            print "Device not found!\n"

if __name__ == "__main__":
    main()
