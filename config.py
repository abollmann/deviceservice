import os

SECRET_KEY = os.environ.get('SECRET_KEY', '7j@+pza(6(=*)$7zsb)bu*$f$fu1kcs*-oz78chs&r(x)@fu-d')
DEBUG = os.environ.get('DEBUG', False)
APP_HOST = os.environ.get('APP_HOST', '0.0.0.0')

MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')
MONGO_PORT = os.environ.get('MONGO_PORT', '27017')
MONGO_USER = os.environ.get('MONGO_USER', '')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD', '')
MONGO_NAME = os.environ.get('MONGO_NAME', '')

KAFKA_HOST = os.environ.get('KAFKA_HOST', '127.0.0.1')
KAFKA_PORT = os.environ.get('KAFKA_PORT', '9093')
KAFKA_PREFIX = os.environ.get('KAFKA_PREFIX', 'local')

FRAUNHOFER_API_USER = os.environ.get('FRAUNHOFER_API_USER')
FRAUNHOFER_API_PASSWORD = os.environ.get('FRAUNHOFER_API_PASSWORD')
