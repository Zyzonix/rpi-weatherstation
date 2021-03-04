#
# written by @author ZyzonixDev
# published by ZyzonixDevelopments
# -
# date      | Sun Jan 03 2021
# python-v  | 3.5.3
# -
# file      | air_quality.py
# -
# USING FOLLOWING RESSOURCE(S):
# https://github.com/binh-bk/nova_fitness_sds011
# - 
import struct
import serial
import time


# access to values: station.air_quality.AIR_QUALITY().query()

class AIR_QUALITY(object):
       
    # Encoding settings
    HEAD = b'\xaa'
    TAIL = b'\xab'
    CMD_ID = b'\xb4'
    READ = b"\x00"
    WRITE = b"\x01"
    REPORT_MODE_CMD = b"\x02"
    ACTIVE = b"\x00"
    PASSIVE = b"\x01"
    QUERY_CMD = b"\x04"
    SLEEP = b"\x00"
    WORK_PERIOD_CMD = b'\x08'

    # Initialization of sensor connection
    def __init__(self, serial_port="/dev/ttyUSB0", baudrate=9600, timeout=2, use_query_mode=True):
        self.ser = serial.Serial(port=serial_port, baudrate=baudrate, timeout=timeout)
        self.ser.flush()
        self.set_report_mode(active=not use_query_mode)

    # Requesting data
    def _execute(self, cmd_bytes):
        self.ser.write(cmd_bytes)

    # Reading request
    def _get_reply(self):
        """Read reply from device."""
        raw = self.ser.read(size=10)
        try:
            data = raw[2:8]
            if (sum(d for d in data) & 255) != raw[8]:
                return None  #TODO: also check cmd id
            return raw
        except Exception as e:
            print('Error: {}'.format(e))
            return None


    def cmd_begin(self):
        return self.HEAD + self.CMD_ID

    def set_report_mode(self, read=False, active=False):
        cmd = self.cmd_begin()
        cmd += (self.REPORT_MODE_CMD
                + (self.READ if read else self.WRITE)
                + (self.ACTIVE if active else self.PASSIVE)
                + b"\x00" * 10)
        cmd = self._finish_cmd(cmd)
        self._execute(cmd)
        try:
            self._get_reply()
        except Exception as e:
            print('Error while getting reply: {}'.format(e))
            pass

    # Querying request command
    def query(self):
        cmd = self.cmd_begin()
        cmd += (self.QUERY_CMD
                + b"\x00" * 12)
        cmd = self._finish_cmd(cmd)
        self._execute(cmd)

        raw = self._get_reply()
        if raw is None:
            return None  #TODO:
        data = struct.unpack('<HH', raw[2:6])
        pm25 = data[0] / 10.0
        pm10 = data[1] / 10.0
        return pm25, pm10

    # Finishing request
    def _finish_cmd(self, cmd, id1=b"\xff", id2=b"\xff"):
        cmd += id1 + id2
        checksum = sum(d for d in cmd[2:]) % 256
        cmd += bytes([checksum]) + self.TAIL
        return cmd
