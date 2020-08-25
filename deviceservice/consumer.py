from threading import Thread

from bson import ObjectId
from kafka import KafkaConsumer

from deviceservice import logger
from deviceservice.shared.error_handlers import handle_kafka_errors
from deviceservice.model import Device
from config import KAFKA_HOST, KAFKA_PORT, KAFKA_PREFIX
from deviceservice.shared.util import parse_message


class DeviceConsumer(Thread):
    daemon = True

    def run(self):
        consumer = KafkaConsumer(
            F'{KAFKA_PREFIX}-devices-commands',
            bootstrap_servers=[F'{KAFKA_HOST}:{KAFKA_PORT}'],
            client_id=F'{KAFKA_PREFIX}-devices-consumer',
            group_id=F'{KAFKA_PREFIX}-devices-commands')

        for message in consumer:
            handle_message(message)


def handle_get_by_id(data):
    devices = [device.to_dict() for device in Device.objects.raw(data)]
    if not data:
        logger.warn(F'Not found: {data}')
        return {}, 404
    else:
        device = devices[0]
        logger.warn(F'Found {data}')
        return device, 200


def handle_distribute(data):
    tenant_id = ObjectId(data['tenant_id'])
    for device_id in data['device_ids']:
        Device.objects.raw({'_id': ObjectId(device_id)}).update(
            {'$set': {'tenant': tenant_id, 'current_price': 0}})
        logger.warn(F'Updated {device_id}')
    return None, None


def handle_remove(data):
    pass


ALLOWED_MESSAGE_TYPES = ['REMOVE_DEVICES', 'DISTRIBUTE_DEVICES']
METHOD_MAPPING = {'REMOVE_DEVICES': handle_remove,
                  'DISTRIBUTE_DEVICES': handle_distribute}


@handle_kafka_errors
def handle_message(message):
    data, command_type = parse_message(message, ALLOWED_MESSAGE_TYPES)
    METHOD_MAPPING[command_type](data)
