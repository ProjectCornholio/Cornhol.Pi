import smbus
import time

class ColorSensor():
    def __init__(self):
        print "Initializing Color Sensor..."
        self.__bus = smbus.SMBus(1)
        self.__bus.write_byte(0x29,0x80|0x12)
        ver = self.__bus.read_byte(0x29)

        if ver == 0x44:
            print "Version verified"
            self.__bus.write_byte(0x29, 0x80|0x00) # enable register
            self.__bus.write_byte(0x29, 0x01|0x02) # (power on | rgb sensor en)
            self.__bus.write_byte(0x29, 0x80|0x14) # read reg starts with 0x14
            self.__prev_red = 0
            self.__prev_blue = 0
            self.__count = 0
            data = self.__bus.read_i2c_block_data(0x29, 0)

        else:
            print "Err: Could not find device"
        print "Done"
        
    def read(self):
        # read register from color sensor
        data = self.__bus.read_i2c_block_data(0x29, 0)
        clear = data[1] << 8 | data[0]
        red = data[3] << 8 | data[2]
        green = data[5] << 8 | data[4]
        blue = data[7] << 8 | data[6]
        ret_val = (0,0)

        # detected red bag
        # return a tuple of (red,blue)
        if (red - self.__prev_red) > (blue - self.__prev_blue) \
          and (red - self.__prev_red) >= 1000 \
          and self.__count > 1:
            ret_val = (1,0)
            #time.sleep(0.15)

        # detected blue bag
        elif (blue - self.__prev_blue) > (red - self.__prev_red) \
          and (blue - self.__prev_blue) >= 800 \
          and self.__count > 0:
            ret_val = (0,1)
            #time.sleep(0.15)

        #crgb = "c: %s, R: %s, G: %s, B: %s\n" % (clear, red, green, blue)
        #print crgb
        self.__prev_red = red
        self.__prev_blue = blue
        self.__count += 1
        #time.sleep(1)

        return ret_val
        

'''
def read(bus):
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
        return (1,0)
        print "red bag detected!\n"
        #time.sleep(0.15)

    # detected blue bag
    elif (blue - prev_blue) >= 800 \
      and (blue - prev_blue) > (red - prev_red) \
      and count > 0:
        return (0,1)
        print "blue bag detected!\n"
        #time.sleep(0.15)

    #crgb = "c: %s, R: %s, G: %s, B: %s\n" % (clear, red, green, blue)
    #print crgb
    prev_red = red
    prev_blue = blue
    count += 1
    #time.sleep(1)

def main():
    bus = smbus.SMBus(1)
    bus.write_byte(0x29,0x80|0x12)
    ver = bus.read_byte(0x29)
    print hex(ver)

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
            read(bus)

    else:
            print "Device not found!\n"
'''

if __name__ == "__main__":
    sensor = ColorSensor()
    red_cnt = 0
    blue_cnt = 0
    prev_red = red_cnt
    prev_blue = blue_cnt

    while True:
        new_red, new_blue = sensor.read()
        red_cnt += new_red
        blue_cnt += new_blue
        if prev_red != red_cnt or prev_blue != blue_cnt:
            print "RED COUNT: %s\t\nBLUE COUNT:%s\t\n" % (str(red_cnt), str(blue_cnt))
            prev_red = red_cnt
            prev_blue = blue_cnt
