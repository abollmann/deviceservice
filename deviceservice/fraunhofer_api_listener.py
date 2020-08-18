import atexit

import requests
import json

from apscheduler.schedulers.background import BackgroundScheduler
from requests.auth import HTTPBasicAuth

from deviceservice.model import Device
from config import FRAUNHOFER_API_USER, FRAUNHOFER_API_PASSWORD

BASE_URL = F'https://applik-d18.iee.fraunhofer.de:8443/flat/AB%s/measurements/'
ACTIVE_DEVICES = 20


def update_devices():
    for i in range(1, ACTIVE_DEVICES):
        building_id = F'AB{i}'
        response = requests.get(BASE_URL % i,
                                auth=HTTPBasicAuth(username=FRAUNHOFER_API_USER, password=FRAUNHOFER_API_PASSWORD))
        if response.status_code == 200:
            data = json.loads(response.content.decode('utf-8'))
            for device in data['rooms']:
                device_identifier = {'building_id': building_id,
                                     'room_nr': device['roomNr']}
                device_data = {'timestamp': device['temperature']['timestamp'],
                               'temperature': device['temperature']['value'],
                               'meter_value': device['meterValue']['value']}
                device = Device.objects.raw(device_identifier)
                if list(device):
                    device.update({'$set': device_data})
                else:
                    device_data.update(device_identifier)
                    Device(**device_data).save()


scheduler = BackgroundScheduler()
scheduler.add_job(func=update_devices, trigger="interval", hours=1)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())