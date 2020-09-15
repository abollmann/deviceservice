from deviceservice import app
from deviceservice.consumer import DeviceConsumer

from config import APP_HOST
from deviceservice.fraunhofer_api_listener import update_devices

if __name__ == '__main__':
    DeviceConsumer().start()
    update_devices()
    app.run(host=APP_HOST, port=5002)
