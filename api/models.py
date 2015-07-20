from collections import OrderedDict
import datetime
from django.db import models
from django.core.exceptions import ValidationError

VALID_COLOURS = range(4)
VALID_FLASH = [1, 2, 4, 8, 16]
INVALID_HOUSE_CODE_MSG = "Invalid house-code. Recieved: {}, expected XX-XX where XX are uppercase hex numbers"
HOUSE_CODE_NOT_FOUND_MSG = "house-code not found: {}"

# Create your models here.
class HouseCode(models.Model):
    code = models.CharField(primary_key=True, max_length=5)
    relative_humidity = models.IntegerField(choices=[(i, i) for i in range(101)], default=None, null=True, blank=True)
    temperature_opentrv = models.CharField(max_length=6, default=None, null=True, blank=True)
    temperature_ds18b20 = models.CharField(max_length=6, default=None, null=True, blank=True)
    window = models.CharField(max_length=6, choices=[(i, i) for i in ["open", "closed"]], default=None, null=True, blank=True)
    switch = models.CharField(max_length=3, choices=[(i, i) for i in ["off", "on"]], default=None, null=True, blank=True)
    last_updated_all = models.DateTimeField(default=None, null=True, blank=True)
    last_updated_temperature = models.DateTimeField(default=None, null=True, blank=True)
    synchronising = models.CharField(max_length=3, choices=[(i, i) for i in ["off", "on"]], default=None, null=True, blank=True)
    ambient_light = models.IntegerField(choices=[(i, i) for i in range(256)], default=None, null=True, blank=True)

    def __str__(self):
        return str(self.code)

    def is_valid_format(self):
        try:
            assert(len(self.code) ==  5)
            assert(self.code[2] == '-')
            (hex1, hex2) = self.code.split('-')
            hex1 = int(hex1, 16)
            hex2 = int(hex2, 16)
            return True
        except (IndexError, AssertionError, ValueError) as e:
            return False

    def clean(self, *args, **kwargs):
        if not self.is_valid_format():
            raise ValidationError({'code': INVALID_HOUSE_CODE_MSG.format(self.code)})

    def to_dict(self):
        dict_ = OrderedDict()
        dict_['house-code'] = self.code
        dict_['relative-humidity'] = self.relative_humidity
        dict_['temperature-opentrv'] = self.temperature_opentrv
        dict_['temperature-ds18b20'] = self.temperature_ds18b20
        dict_['window'] = self.window
        dict_['switch'] = self.switch
        dict_['last-updated-all'] = self.last_updated_all
        dict_['last-updated-temperature'] = self.last_updated_temperature
        dict_['synchronising'] = self.synchronising
        dict_['ambient-light'] = self.ambient_light
        return dict_
    
class Debug(models.Model):
    state = models.CharField(max_length=3, default="off")

class Led(models.Model):
    colour = models.IntegerField(choices=[(i, i) for i in VALID_COLOURS])
    flash = models.IntegerField(choices=[(i, i) for i in VALID_FLASH])
