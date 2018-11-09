
all: setup_pi bluetoothLE opencv lightsensor

setup_pi:
	sudo sed -i "s/#dtparam=spi=on/dtparam=i2c_arm=on/" /boot/config.txt
	@echo "Pi Setup complete! Please Reboot"

pip:
	sudo apt-get install python-pip -y

bluetoothLE: pip
	sudo apt-get install -y pkg-config
	sudo apt-get install -y libboost-python-dev
	sudo apt-get install -y libboost-thread-dev
	sudo apt-get install -y libbluetooth-dev
	sudo apt-get install -y libglib2.0-dev
	sudo pip install pybluez
	sudo pip install pybluez\[ble\]

opencv: pip
	sudo pip install opencv-python

lightsensor:
	sudo apt-get install -y python-smbus i2c-tools

