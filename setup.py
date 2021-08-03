#
# written by @author ZyzonixDev
# published by ZyzonixDevelopments
# -
# date      | Wed Mar 03 2021
# python-v  | 3.5.3
# -
# file      | setup.py
# file-v    | 1.5 // rework of first stable release, updated pip-packages
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
import platform


class setup(object):

    def checkRoot():
        # checking sudo permissions
        if not os.getuid() == 0:
            print("[ERROR] root / sudo permission required --> sudo python3 setup.py")
            return False
        else:
            print("[INFO] running with root permissions")  

    def checkPythonVersion():
        versionSplit = platform.python_version().split(".")
        ret = True
        if not int(versionSplit[0]) >= 3 or not int(versionSplit[1]) >= 6:
            print("[ERROR] wrong python-version (current version: " + platform.python_version() +") --> please use/install python3.6+")
            ret = False
        else:
            print("[INFO] python version matches the requirements")
        return ret

    def checkPackages():
        packages = ["datetime", "configparser", "threading", "smbus", "sqlite3", "ftplib", "traceback", "os", "psutil", "serial", "fastapi", "uvicorn"]
        ret = True
        
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
                ret = False
        return ret
        

    def setValues(self):
        print("[INFO] please fill in the next questions, typing nothing will change nothing (preset values are being kept)\n")
        sec = str(input("Please enter the duration between each run: (preset: 300 sec)\n"))
        sync_time = str(input("Please enter the duration between each server sychronisation: (preset: 3600 sec / 1h)\n"))
        air_quality_time = str(input("Please enter the duration between each run of the air_quality measurement: (preset: 8 loops are being skipped (2*300 = 10 min))\n"))
        prebaseFilePath = str(input("Please enter the home directory: (preset: " + os.getcwd() + "| typing nothing will set the current directory)\n"))
        SyncEnabled = str(input("Should the syncronisation to a FTPShare be enabled? (y/n) \n"))
        if SyncEnabled == "y":
            FTPShareIP = str(input("Please enter the IP of your FTPShare: (preset: 192.168.8.3)\n"))
            FTPuname = str(input("Please enter the username for your FTP Share: (leave empty if no username is required)\n"))
            FTPpwd = str(getpass.getpass("Password for FTP Share [letters hidden]: (type nothing if no password is required) \n"))
            FTPShareLoc = str(input("Please enter the home database directory of your FTPShare:\n"))
        cp = ConfigParser()
        cp.read(os.getcwd() + "/setup/config.ini")
        conf = cp["CONFIGURATION"]
        # the following part could also be solved more elegant/dynamic...
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
            db["baseFilePath"] = os.getcwd()
            self.baseFilePath = db["basefilepath"]
        if SyncEnabled == "y":
            db["sync_enabled"] = "True"
            if FTPShareIP != "":    
                db["FTPShareIP"] = FTPShareIP
            if FTPuname != "":
                db["uname"] = FTPuname  
            if FTPpwd != "":
                db["pwd"] = FTPpwd       
            if FTPShareLoc != "":
                db["FTPShareLoc"] = FTPShareLoc
        else:
            db["sync_enabled"] = "False"
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
            print("[INFO] system service already installed properly") 
            
        if not os.path.exists("/lib/systemd/system/livedataProvider.service"):
            os.system("sudo cp " + os.getcwd() + "/setup/livedataProvider.service /lib/systemd/system/")
            print("[INFO] installing livedata service")
        else:
            print("[INFO] livedata service already installed properly")  

    def startService():
        if str(input("[INFO] start service now? (y/n) \n")) == "y":
            os.system("sudo systemctl start station.service")   
            print("[INFO] started station.service")
        else:
            print("[INFO] didn't start the service")    
            
        if str(input("[INFO] start livedata service now? (y/n) \n")) == "y":
            os.system("sudo systemctl start livedataProvider.service")   
            print("[INFO] started livedataProvider.service")
        else:
            print("[INFO] didn't start the service") 


    def enableService():
        if str(input("[INFO] make weather station service enabled? (y/n) \n")) == "y":
            os.system("sudo systemctl enable station.service")   
            print("[INFO] enabled station.service to start at boot")
        else:
            print("[INFO] cancelled autostart")
            
        if str(input("[INFO] make livedata service enabled? (y/n) \n")) == "y":
            os.system("sudo systemctl enable livedataProvider.service")   
            print("[INFO] enabled livedataProvider.service to start at boot")
        else:
            print("[INFO] cancelled autostart")  

    def __init__(self):
        setupSuccessful = True
        if setup.checkRoot() == False:
            return
        if setup.checkPythonVersion() == False:
            return
        try:
            self.setValues()
            self.createFolders()
            if setup.checkPackages() == False:
                print("\n--------------------------------------------\n- something went wrong \n- please check if all required python-packages \nare installed properly\n--------------------------------------------\n")                    
                setupSuccessful = False
            setup.checkService() 
            setup.startService()
            setup.enableService() 
        except:
            print("\n--------------------------------------------\nsomething went wrong - please retry! stacktrace:\n--------------------------------------------\n")    
            traceback.print_exc()
        if setupSuccessful:
            print("\n-------------------------\nSETUP COMPLETED SUCESSFULLY\n-------------------------\n")    
        else:
            print("\n-------------------------\nSETUP COMPLETED WITH ERRORS\n-------------------------\n")    

        
        
if __name__ == "__main__":
    setup()   
