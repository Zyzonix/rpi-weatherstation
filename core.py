#
# written by @author ZyzonixDev
# published by ZyzonixDevelopments
# -
# date      | Sun Jan 03 2021
# python-v  | 3.5.3
# -
# file      | core.py
# file-v    | 1.3 // inserted new sync validation // stable release / revision 1
#
# USING FOLLOWING RESSOURCE(S):
# 
# https://zetcode.com/python/ftp/
# https://pythontic.com/ftplib/ftp/nlst
# https://www.thepythoncode.com/article/download-and-upload-files-in-ftp-server-using-python
# https://thispointer.com/compare-get-differences-between-two-lists-in-python/  
#
#--------------------------------------

from datetime import date, datetime
from configparser import ConfigParser
import sys
import threading
import smbus
import sqlite3
import ftplib
import traceback
import os
import station.air_stats as ais
import station.air_quality as aiq
import sqldb as dbHandler
import station.sys_stats as sysStats


# SYSTEM SERVICE:
# name: station.service (located in: /lib/systemd/system)
# twinfile in /home/pi/weatherstation/sservice called station.service
# check status: sudo systemctl status station.service

# writing console output to console and logfile
class LogWriter(object):
    def __init__(self, *files):
        # retrieving files / output locations
        self.files = files
    def write(self, obj):
        # getting files (logfile / console (as file))
        for file in self.files:
            file.write(obj)
            file.flush()
    def flush(self):
        # flushing written lines/files
        for file in self.files:
            file.flush()



# data import / measurement / saving 
class handleMeasurement(object):

    # getting db formatted date/time
    def getTime(self):
        curTime = "" + str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        return curTime

    # retrieving data
    def retrieveData(self):
        # creating/initializing next autorun
        threading.Timer(self.MES_TIME, handleMeasurement.retrieveData, [self]).start()
        print(self.getTime(), "installed next autorun --> collecting data")
        self.PARTICULATE_MATTER_MES = self.PARTICULATE_MATTER_MES + 1

        dbConnection = dbHandler.getDBConnection(self)
        try:
            # getting values
            temperature = ais.getTemperature()
            # splitting temperature array (see station.air_stats.getTemperature() for further information)
            f_temperature = temperature[0]
            raw_temperature = temperature[1]
            humidity = ais.getHumidity()
            pressure = ais.getPressure()
            print(self.getTime(), "collected air_stats data successfully: temperature (°C):", f_temperature, ", humidity (%):", humidity,", pressure (hPa):", pressure)
            cpu_usage, ram_usage, cpu_temp = sysStats.getSysStats(self)
            print(self.getTime(), "collected system data successfully: cpu-usage (%):", cpu_usage, ", ram-usage (%):", ram_usage, ", cpu-temperature (°C):", cpu_temp)
            
            # building sqlite command (previous version resulted in error [str max 3 values]) 
            # SQL changes type from string back to integer when pasting into db 
            cmdbuilder = "'" + handleMeasurement.getTime(self) + "', "
            cmdbuilder += str(f_temperature) + ", "
            cmdbuilder += str(raw_temperature) + ", " 
            cmdbuilder += str(humidity) + ", " 
            cmdbuilder += str(pressure) + ", "
            cmdbuilder += str(cpu_usage) + ", "
            cmdbuilder += str(ram_usage) + ", "
            cmdbuilder += str(cpu_temp)
            
            # storing data
            dbHandler.insertData(self, dbConnection, self.airstable, cmdbuilder)
        except:
            print(self.getTime(), "something went wrong while collecting airstats data")
            traceback.print_exc()

        if self.PARTICULATE_MATTER_MES == self.AIQ_TIME:
            try:
                # import class (seperate self statement required)
                airquality = aiq.AIR_QUALITY()
                pm025, pm100 = airquality.query()
                print(self.getTime(), "collected air_quality data successfully: pm2.5:", pm025, "pm10:", pm100)

                cmdbuilder = "'" + handleMeasurement.getTime(self) + "', "
                cmdbuilder += str(pm025) + ", "
                cmdbuilder += str(pm100)

                # storing data
                dbHandler.insertData(self, dbConnection, self.airqtable, cmdbuilder)
            except:
                print(self.getTime(), "something went wrong while collecting airquality data")
                traceback.print_exc()   
            self.PARTICULATE_MATTER_MES = 0


        dbHandler.closeDBConnection(self, dbConnection)
        #print("\n")    

# syncing db files to smb share
class dbUpload(object):
    
    # syncing missing files
    def syncMissing(self, mfileList, ftpConnection):
        leftToSync = mfileList
        try:
            for sfile in leftToSync:
                # checking for daily file
                if sfile == str(date.today()) + ".db":
                    print(self.getTime(), "syncing daily db to daily-folder")
                    leftToSync.remove(sfile)
                    ftpConnection.cwd("daily/")
                    try:
                        for file in ftpConnection.nlst():
                            ftpConnection.delete(file)
                    except:
                        pass
                    uploadCMD = "STOR " + sfile
                    file = open(self.baseFilePath + "db/" + sfile, "rb")
                    # uploading to ftp share
                    ftpConnection.storbinary(uploadCMD, file)
                    ftpConnection.cwd("..")

                else:
                    print(self.getTime(), "syncing the following database to ftp share: " + sfile)
                    leftToSync.remove(sfile)
                    try:
                        ftpConnection.delete(sfile)
                    except:
                        pass
                    uploadCMD = "STOR " + sfile
                    file = open(self.baseFilePath + "db/" + sfile, "rb")
                    # uploading to ftp share
                    ftpConnection.storbinary(uploadCMD, file)
            # checking if all databases have been synced, if not --> rerun (throwed an error before [some db's were left out], reason unknown - this method prevents this failure)
            if len(leftToSync) != 0:
                self.syncFinished = False
                dbUpload.syncMissing(self, leftToSync, ftpConnection)
                return
            else:
                self.syncFinished = True      
            # confirming that sync is finished       
            print(self.getTime(), "syncing successful - all databases have been synced\n")    
        except:
            print(self.getTime(), "something went wrong - was not able to sync missing databases\n")
            self.syncFinished = False
            traceback.print_exc()
        self.syncFinished = True  
        ftpConnection.quit()

    # checking if ftp db storage equals local db storage
    def checkContent(self, rFileList, ftpConnection):
        # retrieving local db storage + filesizes
        localFileList = []
        localFileSizeList = {}
        for file in os.listdir(self.baseFilePath + "db/"):
            localFileList.append(file)
            localFileSizeList[file] = os.path.getsize(self.baseFilePath + "db/" + file)
        # retrieving remote db storage + filesizes
        remoteFileList = rFileList
        remoteFileSizeList = {}
        ftpConnection.voidcmd('TYPE I')
        for file in remoteFileList:
            try:
                remoteFileSizeList[file] = ftpConnection.size(file)
            # preventing error --> no size of daily-folder
            except:
                pass

        # file sync list
        toSync = []

        # comparing filesizes on local and remote storage
        for file in localFileSizeList.keys():
            # case 1: file doesn't exist on ftp share
            if not file in remoteFileSizeList.keys():
                toSync.append(file)
            # case 2: file exists in both storages
            elif not remoteFileSizeList[file] == localFileSizeList[file]:
                toSync.append(file)
        # returns filelist
        return toSync

    # getting available files
    def getFTPContent(self, ftpConnection):
        # changing directory to specified db storage
        ftpConnection.cwd(self.FTPshareLoc)
        # retrieving available files
        existingFiles = []
        for filename in ftpConnection.nlst():
            existingFiles.append(filename)
        print(self.getTime(), "retrieved existing files of '" + self.FTPshareLoc + "' (number of existing files: " + str(len(existingFiles)) + ")") 
        return existingFiles
        #dbUpload.checkContent(self, existingFiles, ftpConnection)
    
    # initializes a ftp connection
    def getFTPConnection(self):
        if self.syncFinished == False:
            print(self.getTime(), "last syncing process hasn't been finished yet\n")
            return False, 0
        try: 
            ftpConnection = ftplib.FTP(self.FTPServerIP)
            # logs in into the ftp share
            ftpConnection.login(self.FTPuname, self.FTPpwd)
            print(self.getTime(), "ftp connection successful, welcomemsg: " + ftpConnection.getwelcome())
            # starting sycing process
            self.syncFinished = False   
            return True, ftpConnection
        except:
            print(self.getTime(), "something went wrong - was not able to initialize a ftp connection to: " + self.FTPServerIP + " - server may be offline\n")
            return False, 0 
            # prints stack trace
            #traceback.print_exc()   
    
    # validates all databases on ftp shares (preventing corrupted dbs)
    # sync handler
    def handleSync(self):
        threading.Timer(self.SYNC_TIME, dbUpload.handleSync, [self]).start()
        print(self.getTime(), "scheduled next autorun for syncing databases to ftp share")
        connectionEstablished, ftpConnection = dbUpload.getFTPConnection(self)
        if connectionEstablished:
            existingFiles = dbUpload.getFTPContent(self, ftpConnection)
            leftToSync = dbUpload.checkContent(self, existingFiles, ftpConnection)
            dbUpload.syncMissing(self, leftToSync, ftpConnection)

# core class - sensor setup, data controlling, database intialization/setup, threading setup
class Core(object):

    # console time service
    def getTime(self):
        curTime = "[" + str(datetime.now().strftime("%H:%M:%S")) + "]"
        return curTime

    # writing console to log
    def writeLog(self):
        self.logFile = open(self.baseFilePath + "logs/" + str(date.today()) + "_" + str(datetime.now().strftime("%H-%M-%S")) + "_log.txt", "w")
        sys.stdout
        sys.stdout = LogWriter(sys.stdout, self.logFile)

    def __init__(self):
        # saving ressources global (like public) // retrieving missing from config file
        configImport = ConfigParser()
        # os.getcwd() returns execution directory
        configImport.read(os.getcwd() + "/setup/config.ini")
        # importing config data
        self.baseFilePath = configImport["DATABASE"]["baseFilePath"]
        self.FTPServerIP = configImport["DATABASE"]["FTPServerIP"]
        self.FTPshareLoc = configImport["DATABASE"]["FTPShareLoc"]
        self.MES_TIME = int(configImport["CONFIGURATION"]["seconds"])
        self.SYNC_TIME = int(configImport["CONFIGURATION"]["sync_time"])
        self.AIQ_TIME = int(configImport["CONFIGURATION"]["air_quality_time"])
        self.FTPuname = configImport["DATABASE"]["uname"]
        self.FTPpwd = configImport["DATABASE"]["pwd"]
        self.syncFinished = True
        # initializing log
        self.writeLog()
        # values for protection of the particulate matter sensor (meassurement only every 2min)
        self.PARTICULATE_MATTER_MES = 0
        print("\n" + self.getTime(), "running core application \n")
        # running measurement
        handleMeasurement.retrieveData(self)
        # initializing db sync with 5 seconds delay (prevents corrupted databases through double access)
        threading.Timer(5, dbUpload.handleSync, [self]).start()

    


if __name__ == '__main__':
    Core()    
