# Raspberry Pi weather station

[![Version](https://img.shields.io/badge/Version-2.0-orange)]() 
[![Python-Version](https://img.shields.io/badge/Python-3.7.3-blue)]()
[![OS-Type](https://img.shields.io/badge/OS%20Type-Linux-blue)]()
[![Last updated](https://img.shields.io/badge/Last%20updated-28/07/2021-orange)]()
[![Development completed](https://img.shields.io/badge/Development%20completed-true-darkgreen)]()
[![Tests passed](https://img.shields.io/badge/Tests%20passed-false-red)]()

### Table of content
* [The project](#the-project)
* [Requirements](#requirements)
* [Installation](#installation)
* [Controlling](#controlling)
* [About the project](#about-the-project)

### The project
Weather station software developed in Python3.5+ for BME280 and SDS011 sensors.
The software can collect the following data: 
- Temperature
- Humidity
- Pressure
- Concentration of dust particles 

The station can additionally provide livedata for the webinterface through a FastAPI-Webserver (Python3.6+ req.).
The whole software can be controlled with the included Makefile.

Please note that the whole project is licensed under the GNU General Public License.


### Requirements:
* Python 3.7.3 installed
* Sensors:
  - Bosch BME280 
  - Nova PM Sensor SDS011
* Raspberry Pi with Raspberry Pi OS (Desktop/Lite v.10+ [Buster])(Linux) installed 
  - it doesn't matter which Pi from the Pi-family it actually is
  - the device just needs one USB port and a GPIO
  - (developed on: Raspberry Pi 3A+)
* Root permissions
* access to a FTP compatible networkshare (for database storing)

### Installation:
**Please note that all python commands must be run in Python3.5+! (The livedata-server requires Python3.6+) Python3.7 is recommmended, check your pythonversion using:**
```
$ python3 --version
```

Firstly clone this repository to your device using git and this command:
```
$ git clone https://github.com/Zyzonix/rpi-weatherstation.git
$ cd rpi-weatherstation/
```
Run the setup script as root (initializing setup via python3 is recommended):
##### Please notice, that all required commands are accessible through make.
```
$ sudo python3 setup.py
```
or
```
$ sudo make install
```
Fill in the questions, check the console output of the setup script if there are no errors displayed, then the setup process was successful and the weather station software is installed properly.

### Controlling
Initializing a testrun:
```
$ python3 core.py
```

##### If you used the tutorial above to set up the software, then system services are used to remote control it:
Type ``` make ``` to show the helpmenu
##### General commands:
Command | Description
--- | ---
``` $ sudo make install ``` | Installs the core-software aswell as the livedataProvider and it's services
``` $ sudo make uninstall ``` | Removes the whole software including all services from the device 

##### Weather station commands:
Command | Description
--- | ---
``` $ sudo make start-station ``` | Starts the core-software (not required if the service is enabled)
``` $ sudo make check-station ``` / ``` $ sudo make station-status ``` | Shows the status of the core-software-service
``` $ sudo make stop-station ``` | Stops the service
``` $ sudo make enable-station ``` | Enables autostart at boot
``` $ sudo make disable-station ``` | Disables autostart at boot

##### LivedataProvider commands:
Command | Description
--- | ---
``` $ sudo make start-livedata ``` | Start the livedataProvider-service (not required if the service is enabled)
``` $ sudo make check-livedata ``` / ``` $ sudo make livedata-status ``` | Shows the status of the livedata-Server
``` $ sudo make stop-livedata ``` | Stops the livedataProvider-service
``` $ sudo make enable-livedata ``` | Enables autostart at boot
``` $ sudo make disable-livedata ``` | Disables autostart at boot

### About the project
This software is part of a school project developed by Zyzonix. It's goal was the development of an executeable software, that can retrieve environmental data, write these datasets into databases and display the stored data into graphs on a webserver. 
(This repository only contains the first part, the webserver (second part) won't be published here within this repository, it can be found under Zyzonix/rpi-weatherstation-web)

README-version: 1.8
