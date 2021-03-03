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

# retrieving system statistics
def getSysStats(self):
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    cput = cput = float(open('/sys/class/thermal/thermal_zone0/temp').read())/1000
    return cpu, ram, cput
