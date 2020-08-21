import json

from deviceservice.shared.exceptions import KafkaMessageException


def parse_message(message, allowed_types):
    message = json.loads(message.value.decode('utf-8'))
    message_id = message['id']
    if not all(key in message for key in ['command_type', 'data']):
        raise KafkaMessageException('JSON-Object with "id", "command_type" and "data" expected.', message_id)

    command_type = message['command_type']
    if not any(command == command_type for command in allowed_types):
        raise KafkaMessageException(F'command_type must be either {", ".join(allowed_types)} .',
                                    message_id)
    data = message['data']
    data = data if isinstance(data, dict) else json.loads(data)
    return data, command_type, message_id
