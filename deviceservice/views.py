from bson import ObjectId

from deviceservice import app, logger
from deviceservice.model import Device
from deviceservice.shared.json_encoder import encode_json

DEVICES_BASE_PATH = '/api/devices'


@app.route(DEVICES_BASE_PATH, methods=['GET'])
def get_all():
    devices = [device.to_dict() for device in Device.objects.all()]
    logger.warn(F'Found {len(devices)} entries')
    return encode_json(devices), 200


@app.route(F'{DEVICES_BASE_PATH}/<tenant_id>', methods=['GET'])
def get_by_id(tenant_id):
    devices = [device.to_dict() for device in Device.objects.raw({'tenant': ObjectId(tenant_id)})]
    if not devices:
        logger.warn(F'Not found: {devices}')
        return {}, 404
    else:
        device = devices[0]
        logger.warn(F'Found {device}')
        return device.to_dict(), 200

