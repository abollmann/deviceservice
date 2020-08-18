class KafkaMessageException(Exception):

    def __init__(self, message, message_id, status_code=400):
        self.message = message
        self.kafka_response = {'id': message_id,
                               'status_code': status_code,
                               'data': message}
        super().__init__(self.message)
