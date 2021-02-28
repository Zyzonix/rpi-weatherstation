#
# written by @author ZyzonixDev
# published by ZyzonixDevelopments
# -
# date      | Mon Feb 22 2021
# python-v  | 3.5.3
# -
# file      | sqldb.py
# -
# USING FOLLOWING RESSOURCE(S):
# -
# https://appdividend.com/2020/10/14/how-to-create-sqlite-database-in-python/ 
# -
#--------------------------------------

from datetime import date, datetime
import os
import sqlite3
import traceback
from core import Core 

# DB structure: 
# air_stats: timestamp TEXT, temperature FLOAT, temperature_raw FLOAT, humidity FLOAT, pressure FLOAT, cpu_usage FLOAT, ram_usage FLOAT, cpu_temp FLOAT
# air_quality: timestamp TEXT, air_2_5 FLOAT, air_10 FLOAT

# setting up column description
def dbSetup(self, dbConnection):
    print("\n\n-------------------------\nnew day: " + str(date.today()))
    print(Core.getTime(self), "setting up new database [stats and quality] (daily-based)")
    dbCursor = dbConnection.cursor()
    # saving table names in self
    self.airqtable = "air_quality"
    self.airstable = "air_stats" 
    # creating sql tables
    dbCursor.execute("CREATE TABLE IF NOT EXISTS " + self.airstable + " (timestamp TEXT, temperature FLOAT, temperature_raw FLOAT, humidity FLOAT, pressure FLOAT, cpu_usage FLOAT, ram_usage FLOAT, cpu_temp FLOAT)")
    dbCursor.execute("CREATE TABLE IF NOT EXISTS " + self.airqtable + " (timestamp TEXT, air_2_5 FLOAT, air_10 FLOAT)")
    dbConnection.commit()
    self.db = dbConnection

# returns sqlite3 Database connection | if not exists --> new db will be created
def getDBConnection(self):
    # db path
    self.dbLocation = self.baseFilePath + "db/" + str(date.today()) + ".db"
    # registrating daily db for syncing
    self.dbCurName = str(date.today()) + ".db"
    # checking if db exists
    if not os.path.exists(self.dbLocation):
        # creating db and opening connection to sqlite3 DB
        try:
            connection = sqlite3.connect(self.dbLocation)
            print(Core.getTime(self), "created new database and established connection successfully")
            dbSetup(self, connection)  
            return connection
        except:
            print(Core.getTime(self), "something went wrong - was not able to not initialize a database connection")
            traceback.print_exc()
    else:
        # connection if db already exists
        connection = sqlite3.connect(self.dbLocation)
        print(Core.getTime(self), "connected to database")
        self.airqtable = "air_quality"
        self.airstable = "air_stats"
        return connection

# insert data into db
def insertData(self, connection, table, content):
    cursor = connection.cursor()
    cmd = "INSERT INTO " + table + " VALUES (" + content + ")"
    cursor.execute(cmd)
    connection.commit()

# closes the database connection
def closeDBConnection(self, connection):
    connection.close()
    print(Core.getTime(self), "closed database connection\n")        
