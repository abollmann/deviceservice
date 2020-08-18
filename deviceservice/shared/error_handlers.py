from functools import wraps

from deviceservice import logger
from deviceservice.producer import produce_data
from deviceservice.shared.exceptions import KafkaMessageException


def handle_kafka_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as error:
            if isinstance(error, KafkaMessageException):
                produce_data(error.kafka_response)
            logger.error(error)

    return decorated_function

