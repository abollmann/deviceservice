from flask import Flask, logging
from flask.logging import default_handler
from pymodm import connect

from deviceservice.shared.json_encoder import ImprovedJSONEncoder
from deviceservice.shared.logging_handler import LoggingHandler
from deviceservice.fraunhofer_api_listener import scheduler
from config import *

app = Flask(__name__)
app.config.from_pyfile('../config.py')

# LOGGING CONFIG
logger = logging.create_logger(app)
logger.removeHandler(default_handler)
logger.addHandler(LoggingHandler())

# DATABASE CONFIG
credentials = F'{MONGO_USER}:{MONGO_PASSWORD}@' if MONGO_USER and MONGO_PASSWORD else ''
auth_source = '?authSource=admin' if credentials else ''
mongo_uri = F'mongodb://{credentials}{MONGO_HOST}:{MONGO_PORT}/devops2020db{auth_source}'
print(mongo_uri)
connect(mongo_uri)

# UTIL CONFIG
json_encoder = ImprovedJSONEncoder()

import deviceservice.fraunhofer_api_listener
