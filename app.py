from deviceservice import app
from deviceservice.consumer import DeviceConsumer

from config import APP_HOST

if __name__ == '__main__':
    DeviceConsumer().start()
    app.run(host=APP_HOST, port=5002)
