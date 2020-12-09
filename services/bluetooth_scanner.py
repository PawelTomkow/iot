# usage: python scan_connect.py
from __future__ import print_function

from typing import List, Any

from mbientlab.metawear import MetaWear
from mbientlab.metawear.cbindings import *
from mbientlab.warble import *
from time import sleep

import platform
import six

from ENVIRONMENT_VARIABLES import DEBUG_BLUETOOTH, DEVICE_NAME
from services.logger import start_debug, end_debug


class BluetoothManager:
    metawear_list: List[str]

    def scan_meatwear(self):
        print("scanning for devices...")
        devices = {}

        def handler(result):
            if result.name in devices:
                devices[result.name].append(result.mac)
            else:
                devices[result.name] = [result.mac]

        BleScanner.set_handler(handler)
        BleScanner.start()

        sleep(10.0)
        BleScanner.stop()

        if DEBUG_BLUETOOTH:
            start_debug()
            i = 0
            for name, addresses in six.iteritems(devices):
                print(f"[{i}] {name}")
                for address in list(set(addresses)):
                    print(address)
                i += 1
            end_debug()

        self.metawear_list = self.filter_metawear_devices(devices[DEVICE_NAME])

    def filter_metawear_devices(self, metawear_list):
        return list(set(metawear_list))

    def get_devices(self):
        return self.metawear_list
