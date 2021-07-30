#!/usr/bin/python3
#
# written by @author ZyzonixDev
# published by ZyzonixDevelopments 
# -
# date      | 20/06/2021
# python-v  | 3.7.3
# -
# file      | WS-web_livedataProvider.py
# project   | rpi-weatherstation
# project-v | 0.9.0
#

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime, date
import station.air_stats as ais

# creates webserverinstance
app = FastAPI()

# webserverconfig
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# timeservice for consoleoutput
def getTime():
    curTime = "[" + str(datetime.now().strftime("%H:%M:%S")) + "]"
    return curTime

# subpage/fastapi register for data request
@app.get("/")
async def datarange():
    print(getTime(), "answering data request")
    status = 1000
    try:
        temperature = ais.getTemperature()
    except Exception as e:
        print(e)
        status += 1
    try:
        humidity = ais.getHumidity()
    except Exception as e:
        print(e)
        status += 10
    try:
        pressure = ais.getPressure()
    except Exception as e:
        status += 100
    
    timestamp = str(date.today()) + "|" + str(datetime.now().strftime("%H:%M:%S"))

    toJSON = [{"status": 1000, "data":[timestamp, temperature, humidity, pressure]}]
    return toJSON

# initialize webserver --> port 8000 --> runnning on localhost --> eth0/wlan0 ipv4
def serverInit():
    uvicorn.run(app, port=8001, host='0.0.0.0')

# initialize script
if __name__ == "__main__":
    print(getTime(), "started coreServer-App")
    serverInit()
