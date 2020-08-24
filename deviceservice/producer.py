from kafka import KafkaProducer

from config import KAFKA_HOST, KAFKA_PORT, KAFKA_PREFIX

producer = KafkaProducer(
    bootstrap_servers=[F'{KAFKA_HOST}:{KAFKA_PORT}'],
    client_id=F'{KAFKA_PREFIX}-devices-producer')


def produce_log(msg):
    value = bytes(msg, encoding='utf-8')
    producer.send(F'{KAFKA_PREFIX}-devices-logs', value=value)
