from time import sleep

from services.bluetooth_scanner import BluetoothManager
from services.stream_acc import StreamAcc
from storage.influxdb_store import DatabaseStore

test_in_s = 100000.0

btManager = BluetoothManager()
btManager.scan_meatwear()
metawear_devices = btManager.get_devices()

db_stor= DatabaseStore()
db_stor.connect()

stream_acc = StreamAcc(db_stor)
# stream_acc.init_multidevices(['D1:BC:EC:14:F1:98'])
stream_acc.init_multidevices(metawear_devices)
stream_acc.start_test(test_in_s)

