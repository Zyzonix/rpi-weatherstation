#
# written by @author ZyzonixDev
# published by ZyzonixDevelopments 
# -
# date      | 13/04/2021
# type      | Makefile
# -
# file      | Makefile
# project   | rpi-weatherstation
# version   | 2.5
# 
all: help

# WEATHER STATION:

# initializing setup --> fw. to python script
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
	# removing current dir --> pwd
	sudo rm -rf $(pwd)
	@echo ""
	@echo "uninstallation of rpi-weatherstation finished"
	@echo ""

# starting station service
start-station:
	@echo "starting weather station service"
	@echo
	sudo systemctl start station.service

# stopping station service
stop-station:	
	@echo "stopping weather station service"
	@echo ""
	sudo systemctl stop station.service

# installing service
enable-station:
	@echo "installing weather station service"
	@echo ""
	sudo systemctl enable station.service

# uninstalling service
disable-station:
	@echo "uninstalling weather station service"
	@echo ""
	sudo systemctl disable station.service

station-status: check-station
# check status of service
check-station: 
	@echo "checking weather station status"
	@echo ""
	@echo "the following error is due to the command - don't worry"
	@echo ""
	sudo systemctl status station.service

# LIVEDATA SERVICE:

# starting livedata service
start-livedata:
	@echo "starting livedataProvider service"
	@echo
	sudo systemctl start livedataProvider.service

# stopping livedata service
stop-livedata:	
	@echo "stopping livedataProvider service"
	@echo ""
	sudo systemctl stop livedataProvider.service

# installing livedata service
enable-livedata:
	@echo "installing livedataProvider service"
	@echo ""
	sudo systemctl enable livedataProvider.service

# uninstalling livedata service
disable-livedata:
	@echo "uninstalling livedataProvider service"
	@echo ""
	sudo systemctl disable livedataProvider.service

station-livedata: check-livedata
# check status of livedata service
check-livedata: 
	@echo "checking livedataProvider status"
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
	@echo "- sudo make start-station..........starts the system service"
	@echo "- sudo make stop-station...........stops the system service"
	@echo "- sudo make enable-station.........installs the system service"
	@echo "- sudo make disable-station........uninstalls the system service"
	@echo "- sudo make check-station..........shows the status of the station system service"
	@echo ""
	@echo "-------------------------- [livedataProvider - HELP] --------------------------"
	@echo ""
	@echo "- sudo make start-livedata.........starts the livedata service"
	@echo "- sudo make stop-livedata..........stops the livedata service"
	@echo "- sudo make enable-livedata........installs the livedata service"
	@echo "- sudo make disable-livedata.......uninstalls the livedata service"
	@echo "- sudo make check-livedata.........shows the status of the livedata system service"
	@echo "---------------------------------------------------------------------------------"
	@echo ""
