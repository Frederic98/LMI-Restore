#!/usr/bin/env python3
import time
import serial, serial.tools.list_ports
from bitsetting import BitSetting, ConfiguredBitSetting
import threading

ScannerSettings = BitSetting('ScannerSettings',
                             [('mode', 2), ('light', 2), ('laser', 2), ('buzzer', 1), ('led', 1),       # 0x00
                              None,                                                                     #
                              ('scan', 1), (None, 5), ('decode_state', 1), None,                        # 0x02
                              ('printsettingcode', 1), ('settingcode', 1), None,                        # 0x03
                              'stabilize_time',                                                         # 0x04
                              'scan_interval',                                                          # 0x05
                              'scan_time',                                                              # 0x06
                              ('sleep_enable', 1), 'sleep_time_h',                                      # 0x07
                              'sleep_time_l',                                                           # 0x08
                              None,
                              'buzzer_freq',                                                            # 0x0A
                              'buzzer_duration',                                                        # 0x0B
                              ('buzzer_level', 1), None,                                                # 0x0C
                              ('data_port', 2),  ('data_format', 2), None,                              # 0x0D
                              (None, 5), ('buzzer_scan', 1), None,                                      # 0x0E
                              *[None]*28,
                              ('baud_l', 5), None,                                                      # 0x2A
                              'baud_h',                                                                 # 0x2B
                              ])


def crc16(data: bytes, poly=0x8408):
    """
    CRC-16-CCITT Algorithm
    https://gist.github.com/oysstu/68072c44c02879a2abf94ef350d1c7c6
    """
    data = bytearray(data)
    crc = 0xFFFF
    for b in data:
        cur_byte = 0xFF & b
        for _ in range(0, 8):
            if (crc & 0x0001) ^ (cur_byte & 0x0001):
                crc = (crc >> 1) ^ poly
            else:
                crc >>= 1
            cur_byte >>= 1
    crc = (~crc & 0xFFFF)
    crc = (crc << 8) | ((crc >> 8) & 0xFF)

    return crc & 0xFFFF


class Scanner:
    CRC = False

    def __init__(self, port, baud=9600):
        self.port = serial.Serial(port, baud)
        self.mutex = threading.RLock()
        # Settings: 179 bytes
        self.settings = ScannerSettings(self.read_data(0x00, 179))  # type: ConfiguredBitSetting
        print(self.settings['data_port'])

        self.settings['mode'] = 1               # 0: manual - 1: command - 2: continuous - 3: sensing
        self.settings['data_port'] = 1          # 0: UART - 1: Keyboard
        self.settings['light'] = 1              # 0: off - 1: auto - 2: on
        self.settings['laser'] = 1              # 0: off - 1: auto - 2: on
        self.settings['led'] = 1                # 0: off - 1: on
        self.settings['buzzer'] = 0             # 0: off - 1: on
        self.settings['decode_state'] = 1
        self.upload_settings()
        self.save_data()

        settings = ScannerSettings(self.read_data(0x00, 179))
        print(settings['data_port'])

    def upload_settings(self):
        try:
            data_start = self.settings.changed.index(True)
            data_stop = len(self.settings.changed) - 1 - self.settings.changed[::-1].index(True)
            return self.send_data(data_start, self.settings.values[data_start:data_stop])
        except ValueError:
            # True not found, so no changed bytes
            pass

    def scan_start(self):
        self.settings['scan'] = 1
        self.upload_settings()

    def scan(self):
        with self.mutex:
            self.scan_start()
            data = ''
            while True:
                c = self.port.read()
                if c == b'\r':
                    break
                data += c.decode()
            return data

    def send_data(self, address, data):
        return self.transfer(0x08, address, data)

    def read_data(self, address, length):
        return self.transfer(0x07, address, [length])

    def save_data(self):
        return self.transfer(0x09, 0x00, [0x00])

    def transfer(self, opcode, address, data):
        with self.mutex:
            data = [0x7E, 0x00,                             # Head1
                    opcode & 0xFF,                          # Types
                    len(data),                              # Data length
                    address >> 8 & 0xFF, address & 0xFF,    # Address
                    *data]                                  # Data
            if self.CRC:
                crc = crc16(bytes(data[2:]))
                data.append(crc & 0xff)
                data.append((crc >> 8) & 0xff)
            else:
                data.extend([0xAB, 0xCD])
            self.port.write(bytes(data))
            rhead = self.port.read(2)
            rtype = self.port.read(1)
            rlen = self.port.read(1)
            rdata = self.port.read(ord(rlen))
            rcrc = self.port.read(2)
            return rdata

    def stop(self):
        with self.mutex:
            self.port.close()


if __name__ == '__main__':
    port = '/dev/ttyS0'
    scanner = Scanner(port, 9600)
    try:
        while True:
            print(scanner.scan())
            time.sleep(1)
    finally:
        print('stopping scanner interface...')
        scanner.stop()
