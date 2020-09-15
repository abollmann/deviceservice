from pymodm import fields, MongoModel
from pymodm.errors import ValidationError


class Device(MongoModel):
    building_id = fields.CharField(required=True)
    room_nr = fields.IntegerField(required=True)
    timestamp = fields.TimestampField(required=True)
    temperature = fields.FloatField(required=True)
    meter_value = fields.FloatField(required=True)
    meter_value_diff = fields.FloatField(default=0)
    tenant = fields.ObjectIdField(required=False, default=None)

    def clean(self):
        if list(Device.objects.raw({'building_id': self.building_id, 'room_nr': self.room_nr})):
            raise ValidationError('building_id and room_nr combined must be unique.')

    def to_dict(self):
        as_dict = self.to_son().to_dict()
        if not self.tenant:
            as_dict['tenant'] = None
        del as_dict['_cls']
        return as_dict
