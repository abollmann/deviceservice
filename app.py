from deviceservice import app
from deviceservice.consumer import ApartmentCommandConsumer

from config import APP_HOST

if __name__ == '__main__':
    ApartmentCommandConsumer().start()
    app.run(host=APP_HOST, port=5002)
