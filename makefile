# dependency makefile

all:

bluetoothLE:
	
numpy:
	sudo apt-get install python3-numpy
	
openCV: numpy
	sudo apt-get install build-essential cmake pkg-config -y
	sudo apt-get install libjpeg8-dev libtiff5-dev libjasper-dev libpng12-dev -y
	sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev -y
	sudo apt-get install libgtk2.0-dev -y
	sudo apt-get install libatlas-base-dev gfortran -y
	git clone https://github.com/opencv/opencv.git -b 3.4.3
	git clone https://github.com/opencv/opencv_contrib.git -b 3.4.3
	# cmake -D CMAKE_BUILD_TYPE=RELEASE \
	#       -D CMAKE_INSTALL_PREFIX=/usr/local \
	#       -D INSTALL_C_EXAMPLES=OFF \
	#       -D INSTALL_PYTHON_EXAMPLES=ON \
	#       -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
	#       -D BUILD_EXAMPLES=ON ..

setup_pi:
	@sudo sed -i "s/#dtparam=spi=on/dtparam=spi=on/" /boot/config.txt
	@sudo apt-get install python3-rpi.gpio -y
	@pip install RPi.GPIO
	@echo "Pi Setup complete! Please Reboot"

spidev:
	# depreciated
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
