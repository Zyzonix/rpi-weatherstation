#
# written by @author ZyzonixDev
# published by ZyzonixDevelopments
# -
# date      | Wed Mar 03 2021
# python-v  | 3.5.3
# -
# file      | setup.py
# file-v    | 1.0 // first stable public release of setup
#
# Ressources:
# https://tutswiki.com/read-write-config-files-in-python/
#
#--------------------------------------
import os
import sys
from configparser import ConfigParser
import traceback
import getpass
import importlib.util


class setup(object):
    def checkRoot():
        # checking sudo permissions
        if not os.getuid() == 0:
            print("[ERROR] root / sudo permission requiered --> sudo python3 setup.py")
            return False
        else:
            print("[INFO] running with root permissions")  

    def checkPackages():
        packages = ["datetime", "configparser", "threading", "smbus", "sqlite3", "ftplib", "traceback", "os"]

        for entry in packages:
            spec = importlib.util.find_spec(entry)
            if entry in sys.modules:
                print("[INFO] " + entry + " already in sys.modules")
            elif spec is not None:
            # If you choose to perform the actual import ...
                module = importlib.util.module_from_spec(spec)
                sys.modules[entry] = module
                spec.loader.exec_module(module)
                print("[INFO] " + entry + " has been imported")
            else:
                print("[ERROR] can't find the "+ entry +" module")
        for entry in packages:
            try:
                globals()[entry] = importlib.import_module(entry)
            except:
                print("[ERROR] something went wrong while importing packages (didn't find: " + entry + ")")


    def setValues(self):
        print("[INFO] please fill in the next questions, typing nothing will change nothing (preset values are being kept)\n")
        sec = str(input("Enter the duration between each run: (preset: 15 sec)\n"))
        sync_time = str(input("Enter the duration between each serversychronisation: (preset: 3600 sec / 1h)\n"))
        air_quality_time = str(input("Enter the duration between each run of the air_quality measurement: (preset: 8 loops are being skipped (8*15 = 2 min))\n"))
        prebaseFilePath = str(input("Enter the home directory: (preset: /home/pi/rpi-weatherstation | typing nothing will parse current directory)\n"))
        FTPShareIP = str(input("Enter the IP of your FTPShare: (preset: 192.168.8.3)\n"))
        FTPuname = str(input("Please enter the username for your FTP Share:\n"))
        FTPpwd = str(getpass.getpass("Password for FTP Share: (type nothing if no password is required) \n"))
        FTPShareLoc = str(input("Enter the home database directory of your FTPShare:\n"))
        cp = ConfigParser()
        cp.read(os.getcwd() + "/setup/config.ini")
        conf = cp["CONFIGURATION"]
        # the following part could also be solved more elegant...
        if sec != "":
            conf["seconds"] = sec
        if sync_time != "":
            conf["sync_time"] = sync_time
        if air_quality_time != "":
            conf["air_quality_time"] = air_quality_time
        db = cp["DATABASE"]
        if prebaseFilePath != "":
            db["baseFilePath"] = prebaseFilePath
            self.baseFilePath = prebaseFilePath
        else:
            self.baseFilePath = db["basefilepath"]
        if FTPShareIP != "":    
            db["FTPShareIP"] = FTPShareIP
        if FTPuname != "":
            db["uname"] = FTPuname
        else:
            print("[ERROR] Please enter a username for the FTP Share")    
        if FTPpwd != "":
            db["pwd"] = FTPpwd       
        if FTPShareLoc != "":
            db["FTPShareLoc"] = FTPShareLoc
        with open(os.getcwd() + "/setup/config.ini", "w") as configfile:
            cp.write(configfile)
        print("[INFO] wrote data to configfile")

    def createFolders(self):
        if not os.path.exists(self.baseFilePath + "db/"):
            os.system("mkdir db")
        if not os.path.exists(self.baseFilePath + "logs/"):
            os.system("mkdir logs")
        print("[INFO] successfully checked environment (if required folders are existing)")    


    def checkService():
        if not os.path.exists("/lib/systemd/system/station.service"):
            os.system("sudo cp " + os.getcwd() + "/setup/station.service /lib/systemd/system/")
            print("[INFO] installing system service")
        else:
            print("[INFO] system service already installed propertly")    

    def startService():
        if str(input("[INFO] start service now? (y/n) \n")) == "y":
            os.system("sudo systemctl start station.service")   
            print("[INFO] started station.service")
        else:
            print("[INFO] didn't start the service")    


    def enableService():
        if str(input("[INFO] make systemservice enabled? (y/n) \n")) == "y":
            os.system("sudo systemctl enable station.service")   
            print("[INFO] enabled station.service to start at boot")
        else:
            print("[INFO] cancelled autostart")        

    def __init__(self):
        if setup.checkRoot() == False:
            return
        try:
            self.setValues()
            self.createFolders()
            setup.checkPackages()
            setup.checkService() 
            setup.startService()
            setup.enableService() 
        except:
            traceback.print_exc()
        print("\n----------------\nSETUP COMPLETED\n----------------\n")    
        






if __name__ == "__main__":
    setup()   