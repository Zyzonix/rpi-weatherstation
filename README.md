# Raspberry Pi Weatherstation

[![Version](https://img.shields.io/badge/Version-1.3-orange)]() 
[![Python-Version](https://img.shields.io/badge/Python-3.5.3-blue)]()
[![last updated](https://img.shields.io/badge/last%20updated-25/07/2021-9cf)]()

Weatherstationsoftware developed in Python3.5 for BME280 and SDS011 sensors.
The software can collect the following data: 
- Temperature
- Humidity
- Pressure
- Concentration of dust particles 

Please note that the whole project is licensed under the GNU General Public License.

### Table of content
* [Requirements](#requirements)
* [Installation](#installation)
* [Controlling](#controlling)
* [About the project](#about-the-project)

### Requirements:
* Python 3.5.3 installed
* Sensors:
  - Bosch BME280 
  - Nova PM Sensor SDS011
* Raspberry Pi with Raspberry Pi OS installed 
  - it doesn't matter which Pi from the Pi-family it actually is
  - the device just needs one USB port and a GPIO
* Root permissions
* access to a FTP compatible networkshare (for database storing)

### Installation:
**Please note that all python commands must be run in Python3!**

Firstly clone this github repository to your device using git and this command:
```
$ git clone https://github.com/Zyzonix/rpi-weatherstation.git
$ cd rpi-weatherstation/
```
Run the setup script as root:
##### Please notice, that all commands are also accessible through make.
```
$ sudo python3 setup.py
```
or
```
$ sudo make setup
```
Fill in the questions, check the console output of the setup script if there are no errors displayed, then the setup process was successful and the weather stations software is installed properly.

### Controlling
If you wish to proceed a test run type
```
$ python3 core.py
```
##### If you used the tutorial above to set up the software, then system services are used to remote control it:
Start the service:
```
$ sudo systemctl start station.service  
```
###### or
```
$ sudo make start
```
View the status of the service:
```
$ sudo systemctl status station.service
```
###### or
```
$ sudo make check
```
Stop the service:
```
$ sudo systemctl stop station.service
```
###### or
```
$ sudo make stop
```
You can enable autostart at boot with:
```
$ sudo systemctl enable station.service
```
###### or
```
$ sudo make enable
```
If you wish to disable autostart type:
```
$ sudo systemctl disable station.service
```
or
```
$ sudo make disable
```

### About the project
This software is part of a school project developed by Zyzonix. It's goal was the development of an executeable software, that can retrieve environmental data, write these datasets into databases and display the stored data into graphs on a webserver. 
(This project just contains the first and second part, the webserver won't be published here within this repository, it can be found under Zyzonix/rpi-weatherstation-web)
