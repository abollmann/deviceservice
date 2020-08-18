import json
from threading import Thread

from kafka import KafkaConsumer

from deviceservice import logger
from deviceservice.producer import produce_data
from deviceservice.shared.error_handlers import handle_kafka_errors
from deviceservice.shared.exceptions import KafkaMessageException
from deviceservice.model import Device
from config import KAFKA_HOST, KAFKA_PORT, KAFKA_PREFIX


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


@handle_kafka_errors
def handle_message(message):
    message = json.loads(message.value.decode('utf-8'))
    message_id = message['id']
    if not all(key in message for key in ['command_type', 'data']):
        raise KafkaMessageException('JSON-Object with "id", "command_type" and "data" expected.', message_id)

    command_type = message['command_type']
    if not any(command == command_type for command in ['GET_ALL', 'GET_BY_FILTER']):
        raise KafkaMessageException('command_type must be either "GET_ALL", "GET_BY_FILTER"',
                                    message_id)

    data = message['data']
    status_code = 200

    if command_type == 'GET_ALL':
        data = [building.to_dict() for building in Device.objects.all()]
        logger.warn(F'Found {len(data)} entries')

    elif command_type == 'GET_BY_ID':
        data = json.loads(data)
        data = [device.to_dict() for device in Device.objects.raw(data)]
        if not data:
            status_code = 404
        else:
            data = data[0]
        logger.warn(F'Found {data}')

    message['data'] = data
    message['status_code'] = status_code
    produce_data(message)
