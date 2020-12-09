from datetime import datetime

from influxdb import InfluxDBClient

import ENVIRONMENT_VARIABLES
from ENVIRONMENT_VARIABLES import INFLUX_DATABASE
from models import Point


class DatabaseStore:
    client: InfluxDBClient = None

    def connect(self):
        self.client = InfluxDBClient(host='localhost', port=18086, username='root', password='root')
        self.client.switch_database(INFLUX_DATABASE)

    def store(self, data):
        json_body = [self.create_influx_obj(x) for x in data]
        # print(json_body)
        self.client.write_points(json_body)

    def create_influx_obj(self, data):
        return ({
                "measurement": "metamon",
                "tags": {
                    "id": data.id
                },
                "time": datetime.utcnow(),
                "fields": {
                    "x": data.x,
                    "y": data.y,
                    "z": data.z,
                }
            })