from bson import ObjectId, Timestamp
from json import JSONEncoder


class ImprovedJSONEncoder(JSONEncoder):
    """ ObjectIds and Timestamps are not encoded by default so we must extend the JSONEncoder. """

    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, Timestamp):
            return obj.time
        return JSONEncoder.default(self, obj)


def encode_json(data):
    return ImprovedJSONEncoder().encode(data)
