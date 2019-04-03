DEV_NUM ?= 1

all: setup_pi bluetoothLE opencv lightsensor

setup_pi:
	sudo sed -i "s/#dtparam=i2c=on/dtparam=i2c_arm=on/" /boot/config.txt
	@echo "Pi Setup complete! Please Reboot"

pip:
	sudo apt-get install python-pip -y

btname:
	sudo echo "PRETTY_HOSTNAME=Cornhol.io_$(DEV_NUM)" > /etc/machine-info

bluetoothLE: pip
	sudo apt-get install -y pkg-config
	sudo apt-get install -y libboost-python-dev
	sudo apt-get install -y libboost-thread-dev
	sudo apt-get install -y libbluetooth-dev
	sudo apt-get install -y libglib2.0-dev
	sudo python -m pip install pybluez
	#sudo pip install pybluez\[ble\]

opencv: pip
	sudo apt-get install python-opencv

lightsensor:
	sudo apt-get install -y python-smbus i2c-tools

no_sleep:
	@echo "@xset s noblank" >> ~/.config/lxsession/LXDE-pi/autostart
	@echo "@xset s off" >> ~/.config/lxsession/LXDE-pi/autostart
	@echo "@xset -dpms" >> ~/.config/lxsession/LXDE-pi/autostart

