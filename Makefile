#
# written by @author ZyzonixDev
# published by ZyzonixDevelopments 
# -
# date      | 13/04/2021
# type      | Makefile
# -
# file      | Makefile
# project   | rpi-weatherstation
# version   | 2.1
# 
all: help

install:
	@echo "installing rpi-weatherstation"
	@echo ""
	sudo python3 setup.py
	@echo "make installation finished"

# removing all entries / files / folders
uninstall:
	@echo ""
	@echo "uninstalling rpi-weatherstation"
	@echo ""
	make stop
	make disable
	sudo rm /lib/systemd/system/station.service
	sudo rm /lib/systemd/system/livedataProvider.service
	sudo rm -rf $(CURDIR)

# starting systemd-service
start-station:
	@echo "starting system service"
	@echo
	sudo systemctl start station.service

# stopping systemd-service
stop-station:	
	@echo "stopping system service"
	@echo ""
	sudo systemctl stop station.service

# installing service
enable-station:
	@echo "installing system service"
	@echo ""
	sudo systemctl enable station.service

# uninstalling service
disable-station:
	@echo "uninstalling system service"
	@echo ""
	sudo systemctl disable station.service

station-status: check-station
# check status of service
check-station: 
	@echo "checking status"
	@echo ""
	@echo "the following error is due to the command - don't worry"
	@echo ""
	sudo systemctl status station.service

# LIVEDATA SERVICE:

# starting livedataservice
start-livedata:
	@echo "starting system service"
	@echo
	sudo systemctl start livedataProvider.service

# stopping livedataservice
stop-livedata:	
	@echo "stopping system service"
	@echo ""
	sudo systemctl stop livedataProvider.service

# installing livedataservice
enable-livedata:
	@echo "installing system service"
	@echo ""
	sudo systemctl enable livedataProvider.service

# uninstalling livedataservice
disable-livedata:
	@echo "uninstalling system service"
	@echo ""
	sudo systemctl disable livedataProvider.service

station-livedata: check-livedata
# check status of livedataservice
check-livedata: 
	@echo "checking status"
	@echo ""
	@echo "the following error is due to the command - don't worry"
	@echo ""
	sudo systemctl status livedataProvider.service

# Helpmenu
# printing all commands of this file
help:
	@echo ""
	@echo "------------------------- [rpi-weatherstation - HELP] -------------------------"
	@echo ""
	@echo "- sudo make install................starts the setup script"
	@echo "- sudo make uninstall..............removes the software from this device"
	@echo "- sudo make start-station..........starts the systemservice"
	@echo "- sudo make stop-station...........stops the systemservice"
	@echo "- sudo make enable-station.........installs the systemservice"
	@echo "- sudo make disable-station........uninstalls the systemservice"
	@echo "- sudo make check-station..........shows the status of the station-systemservice"
	@echo "-------------------------- [livedataProvider - HELP] --------------------------"
	@echo "- sudo make start-livedata.........starts the livedataservice"
	@echo "- sudo make stop-livedata..........stops the livedataservice"
	@echo "- sudo make enable-livedata........installs the livedataservice"
	@echo "- sudo make disable-livedata.......uninstalls the livedataservice"
	@echo "- sudo make check-livedata.........shows the status of the livedata-systemservice"
	@echo "---------------------------------------------------------------------------------"
	@echo ""
