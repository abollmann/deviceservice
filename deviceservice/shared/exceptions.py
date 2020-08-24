class KafkaMessageException(Exception):

    def __init__(self, message, message_id):
        self.message = message
        self.kafka_response = {'id': message_id, 'data': message}
        super().__init__(self.message)

    def __str__(self):
        return str(self.kafka_response)
