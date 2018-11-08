
all:

setup_pi:
	@sudo sed -i "s/#dtparam=spi=on/dtparam=spi=on/" /boot/config.txt
	@echo "Pi Setup complete! Please Reboot"

bluetoothLE:
	@sudo pip install pybluez
	# @git clone https://github.com/pybluez/pybluez
	# @pip install -e .\[ble\] #for ble

opencv:
	@sudo pip install opencv-python

lightsensor:
	@sudo apt-get install -y python-smbus i2c-tools

