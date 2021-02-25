#
# written by @author ZyzonixDev
# published by ZyzonixDevelopments
# -
# date      | Tue Feb 23 2021
# python-v  | 3.5.3
# -
# file      | sys_stats.py
# -
# USING FOLLOWING RESSOURCE(S):
# - 
# -
#--------------------------------------
import psutil

def getSysStats(self):
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    return cpu, ram