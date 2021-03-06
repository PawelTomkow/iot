from time import sleep

from mbientlab.metawear import libmetawear


def reset(device):
    libmetawear.mbl_mw_logging_stop(device.board)
    libmetawear.mbl_mw_logging_clear_entries(device.board)
    libmetawear.mbl_mw_macro_erase_all(device.board)
    libmetawear.mbl_mw_debug_reset_after_gc(device.board)
    print("Erase logger and clear all entries")
    sleep(1.0)

    libmetawear.mbl_mw_debug_disconnect(device.board)
    sleep(1.0)