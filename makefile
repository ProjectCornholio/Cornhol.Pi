# dependency makefile

all:

bluetoothLE:
	
openCV:

setup_pi:
	@sudo sed -i "s/#dtparam=spi=on/dtparam=spi=on/" /boot/config.txt
	@sudo apt-get install python3-rpi.gpio -y
	@pip install RPi.GPIO
	@echo "Pi Setup complete! Please Reboot"

spidev:
	@sudo apt-get install -y python3-dev
	@sudo apt-get install -y python3-spidev
	@git clone https://github.com/Gadgetoid/py-spidev.git
	@cd py-spidev; python3 setup.py install

gpio:
	@sudo apt-get install python3-rpi.gpio -y

spi:
	@sudo sed -i "s/#dtparam=spi=on/dtparam=spi=on/" /boot/config.txt
	@git clone https://github.com/lthiery/SPI-Py.git
	@cd SPI-Py; sudo python3 setup.py install
	@echo "Pi Setup complete! Please Reboot"

MFRC522:
	@git clone https://github.com/mxgxw/MFRC522-python
	@sed -i 's/print "Size: " + str(backData\[0\])/print("Size: " + str(backData\[0\]))/' MFRC522-python/MFRC522.py
	@sed -i 's/print "AUTH ERROR!!"/print("AUTH ERROR!!")/' MFRC522-python/MFRC522.py
	@sed -i 's/print "AUTH ERROR(status2reg \& 0x08) != 0"/print("AUTH ERROR(status2reg \& 0x08) != 0")/' MFRC522-python/MFRC522.py
	@sed -i 's/print "Error while reading!"/print("Error while reading!")/' MFRC522-python/MFRC522.py
	@sed -i 's/print "Sector "+str(blockAddr)+" "+str(backData)/print("Sector "+str(blockAddr)+" "+str(backData))/' MFRC522-python/MFRC522.py
	@sed -i 's/print "%s backdata \&0x0F == 0x0A %s" % (backLen, backData\[0\]\&0x0F)/print("%s backdata \&0x0F == 0x0A %s" % (backLen, backData\[0\]\&0x0F))/' MFRC522-python/MFRC522.py
	@sed -i 's/print "Error while writing"/print("Error while writing")/' MFRC522-python/MFRC522.py
	@sed -i 's/print "Data written"/print("Data written")/' MFRC522-python/MFRC522.py
	@sed -i 's/print "Authentication error"/print("Authentication error")/' MFRC522-python/MFRC522.py
	@sudo cp MFRC522-python/MFRC522.py /usr/lib/python3.5/
