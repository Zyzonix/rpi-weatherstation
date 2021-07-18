#
# written by @author ZyzonixDev
# published by ZyzonixDevelopments 
# -
# date      | 13/04/2021
# type		  | Makefile
# -
# file      | Makefile
# project   | rpi-weatherstation
# version	  | 1.2
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
        sudo rm -rf $(CURDIR)

# starting systemd-service
start:
        @echo "starting system service"
        @echo
        sudo systemctl start station.service

# stopping systemd-service
stop:	
        @echo "stopping system service"
        @echo ""
        sudo systemctl stop station.service

# installing service
enable:
        @echo "installing system service"
        @echo ""
        sudo systemctl enable station.service

# uninstalling service
disable:
        @echo "uninstalling system service"
        @echo ""
        sudo systemctl disable station.service

status: check
# check status of service
check: 
        @echo "checking status"
        @echo ""
        @echo "the following error is due to the command - don't worry"
        @echo ""
        sudo systemctl status station.service

# printing all commands of this file
help:
      @echo ""
      @echo "------------------------- [rpi-weatherstation - HELP] -------------------------"
      @echo ""
      @echo "- sudo make install................starts the setup script"
      @echo "- sudo make uninstall..............removes the software from this device"
      @echo "- sudo make start..................starts the systemservice"
      @echo "- sudo make stop...................stops the systemservice"
      @echo "- sudo make enable.................installs the systemservice"
      @echo "- sudo make disable................uninstalls the systemservice"
      @echo "- sudo make check..................shows the status of the station-systemservice"
      @echo "----------------------------------------------------------------------------------"
      @echo ""
