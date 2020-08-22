from threading import Thread

from kafka import KafkaConsumer

from deviceservice import logger
from deviceservice.producer import produce_data
from deviceservice.shared.error_handlers import handle_kafka_errors
from deviceservice.model import Device
from config import KAFKA_HOST, KAFKA_PORT, KAFKA_PREFIX
from deviceservice.shared.util import parse_message


class ApartmentCommandConsumer(Thread):
    daemon = True

    def run(self):
        consumer = KafkaConsumer(
            F'{KAFKA_PREFIX}-devices-commands',
            bootstrap_servers=[F'{KAFKA_HOST}:{KAFKA_PORT}'],
            client_id=F'{KAFKA_PREFIX}-devices-consumer',
            group_id=F'{KAFKA_PREFIX}-devices-commands')

        for message in consumer:
            handle_message(message)


def handle_get_all(data, message_id):
    devices = [device.to_dict() for device in Device.objects.all()]
    logger.warn(F'Found {len(devices)} entries')
    return devices, 200


def handle_get_by_id(data, message_id):
    devices = [device.to_dict() for device in Device.objects.raw(data)]
    if not data:
        logger.warn(F'Not found: {data}')
        return {}, 404
    else:
        device = devices[0]
        logger.warn(F'Found {data}')
        return device, 200


ALLOWED_MESSAGE_TYPES = ['GET_ALL', 'GET_BY_ID']
METHOD_MAPPING = {'GET_ALL': handle_get_all,
                  'GET_BY_ID': handle_get_by_id}


@handle_kafka_errors
def handle_message(message):
    data, command_type, message_id = parse_message(message, ALLOWED_MESSAGE_TYPES)
    response_data, status_code = METHOD_MAPPING[command_type](data, message_id)
    produce_data({'data': response_data, 'status_code': status_code, 'id': message_id})
