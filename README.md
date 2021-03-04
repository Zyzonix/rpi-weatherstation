# Raspberry Pi Weatherstation

[![Version](https://img.shields.io/badge/Version-1.2%20-orange)]() 
[![Python-Version](https://img.shields.io/badge/Python-3.5.3-blue)]()
[![last updated](https://img.shields.io/badge/last%20updated-04/03/2021-9cf)]()

Weather station software developed in Python3.5 for BME280 and SDS011 sensors.
The software can collect the following data: 
- Temperature
- Humidity
- Pressure
- Concentration of dust particles 

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
```
$ sudo python3 setup.py
```
Fill in the questions, check the console output of the setup script if there are no errors displayed, then the setup process was successful and the weather stations software is installed properly.

### Controlling
If you wish to proceed a test run type
```
$ python3 core.py
```
###### If you used the tutorial above to set up the software, then system services are used to remote control it:
Start the service:
```
$ sudo systemctl start station.service  
```
View the status of the service:
```
$ sudo systemctl status station.service
```
or use the contained bash file (permission granting required):
```
$ sudo chmod +x view_status.sh
$ ./view_status.sh
```
Stop the service
```
$ sudo systemctl stop station.service
```
You can enable autostart at boot with:
```
$ sudo systemctl enable station.service
```
If you wish to disable autostart type:
```
$ sudo systemctl disable station.service
```
### About the project
This software is part of a school project developed by Zyzonix. It's goal was the development of an executeable software, that can retrieve environment data, write it into databases and display the recorded data into graphs on a webserver. 
(This project just contains the first and second part, the webserver won't be published here within this repository)
