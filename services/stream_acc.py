import json
from time import sleep
from typing import List

from mbientlab.metawear import MetaWear, libmetawear, FnVoid_VoidP_DataP, parse_value
from mbientlab.warble import WarbleException

from ENVIRONMENT_VARIABLES import DEBUG_STREAM_ACC, BATCH_STORE
from models.Point import Point
from services import logger
from services.logger import start_debug, end_debug
# from services.reset import reset
from storage.influxdb_store import DatabaseStore


class State:
    strage: DatabaseStore
    def __init__(self, device, strage):
        self.device = device
        self.samples = 0
        self.callback = FnVoid_VoidP_DataP(self.data_handler)
        self.data = []
        self.strage = strage

    def data_handler(self, ctx, data):
        raw_point = parse_value(data)
        point = Point(raw_point.x, raw_point.y, raw_point.z, self.device.address)
        if BATCH_STORE:
            self.data.append(point)
        else:
            self.strage.store([point])
        self.samples += 1

class StreamAcc:
    strage: DatabaseStore
    device_list: List[State]

    def __init__(self, strage: DatabaseStore):

        self.strage = strage

    def init_device(self, device):
        print(f"Configuring device: {device.device.address}")
        # reset(device.device)
        libmetawear.mbl_mw_settings_set_connection_parameters(device.device.board, 7.5, 7.5, 0, 6000)
        sleep(1.5)

        libmetawear.mbl_mw_acc_set_odr(device.device.board, 25.0)
        libmetawear.mbl_mw_acc_set_range(device.device.board, 8.0)
        libmetawear.mbl_mw_acc_write_acceleration_config(device.device.board)



    def init_multidevices(self, devices_mac_list):
        self.device_list = []
        for device_mac in devices_mac_list:
            device = MetaWear(device_mac)
            try:
                device.connect()
            except WarbleException:
                logger.error(f"connect error: {device_mac}")
            print("Connected to " + device.address)
            state_device = State(device, self.strage)
            self.device_list.append(state_device)
            self.init_device(state_device)
            sleep(5.5)

    def start_test(self, time_tests):
        for device in self.device_list:
            logger.info_log(f"Start device: {device.device.address}")
            signal = libmetawear.mbl_mw_acc_get_acceleration_data_signal(device.device.board)
            libmetawear.mbl_mw_datasignal_subscribe(signal, None, device.callback)

            libmetawear.mbl_mw_acc_enable_acceleration_sampling(device.device.board)
            libmetawear.mbl_mw_acc_start(device.device.board)
            sleep(5.0)

        sleep(time_tests)

        for device in self.device_list:
            libmetawear.mbl_mw_acc_stop(device.device.board)
            libmetawear.mbl_mw_acc_disable_acceleration_sampling(device.device.board)

            signal = libmetawear.mbl_mw_acc_get_acceleration_data_signal(device.device.board)
            libmetawear.mbl_mw_datasignal_unsubscribe(signal)
            libmetawear.mbl_mw_debug_disconnect(device.device.board)
            logger.info_log(f"Stop device: {device.device.address}")

        if DEBUG_STREAM_ACC:
            start_debug()
            for s in self.device_list:
                if BATCH_STORE:
                    self.strage.store(s.data)
                print("%s -> %d" % (s.device.address, s.samples))
            end_debug()
