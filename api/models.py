from collections import OrderedDict
import datetime
from django.db import models
from django.core.exceptions import ValidationError

VALID_COLOURS = range(4)
VALID_FLASH = [1, 2, 4, 8, 16]
VALID_RELATIVE_HUMIDITIES = range(101)
VALID_WINDOW_STATES = ['open', 'closed']
VALID_SWITCH_STATES = ['on', 'off']
VALID_SYNCHRONISING_STATES = ['on', 'off']
VALID_AMBIENT_LIGHT_VALUES = range(256)
INVALID_HOUSE_CODE_MSG = 'Invalid input for "house-code". Recieved: {}, expected XX-XX where XX are uppercase hex numbers'
INVALID_RELATIVE_HUMIDITY_MSG = 'Invalid input for "relative-humidity". Received: {}, expected integer value 0 - 100'
INVALID_TEMPERATURE_OPENTRV_MSG = 'Invalid input for "temperature-opentrv". Received: {}, expected a numerical value between 0 and 99.999 with at most 3 decimal places'
INVALID_TEMPERATURE_DS18B20_MSG = 'Invalid input for "temperature-ds18b20". Received: {}, expected a numerical value between 0 and 99.999 with at most 3 decimal places'
INVALID_WINDOW_STATE_MSG = 'Invalid input for "window". Received: {}, expected open/closed'
INVALID_SWITCH_STATE_MSG = 'Invalid input for "switch". Recieved: {}, expected on/off'
INVALID_LAST_UPDATED_ALL_MSG = 'Invalid input for last-updated-all. Received: {}, expected an ISO 8601 date, e.g. 2015-07-22T14:28:00Z'
INVALID_LAST_UPDATED_TEMPERATURE_DATE_MSG = 'Invalid input for last-updated-temperature. '
INVALID_LAST_UPDATED_TEMPERATURE_DATE_MSG += 'Received: {}, expected an ISO 8601 date, e.g. 2015-07-22T14:28:00Z'
INVALID_SYNCHRONISING_STATE_MSG = 'Invalid input for "synchronising". Received: {}, expected on/off'
INVALID_AMBIENT_LIGHT_VALUE_MSG = 'Invalid input for "ambient-light". Received: {}, expected integer 0 - 255'

HOUSE_CODE_NOT_FOUND_MSG = "house-code not found: {}"

# Create your models here.
class HouseCode(models.Model):
    code = models.CharField(primary_key=True, max_length=5)
    relative_humidity = models.IntegerField(choices=[(i, i) for i in VALID_RELATIVE_HUMIDITIES], default=None, null=True, blank=True)
    temperature_opentrv = models.CharField(max_length=6, default=None, null=True, blank=True)
    temperature_ds18b20 = models.CharField(max_length=6, default=None, null=True, blank=True)
    window = models.CharField(max_length=6, choices=[(i, i) for i in VALID_WINDOW_STATES], default=None, null=True, blank=True)
    switch = models.CharField(max_length=3, choices=[(i, i) for i in VALID_SWITCH_STATES], default=None, null=True, blank=True)
    last_updated_all = models.DateTimeField(default=None, null=True, blank=True)
    last_updated_temperature = models.DateTimeField(default=None, null=True, blank=True)
    synchronising = models.CharField(max_length=3, choices=[(i, i) for i in VALID_SYNCHRONISING_STATES], default=None, null=True, blank=True)
    ambient_light = models.IntegerField(choices=[(i, i) for i in VALID_AMBIENT_LIGHT_VALUES], default=None, null=True, blank=True)

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

    @staticmethod
    def temperature_is_valid(temperature):
        try:
            if temperature == None:
                return True
            if len(temperature) > 6:
                raise ValidationError('')
            if "." in temperature:
                (x, y) = temperature.split(".")
                if(len(y) > 3):
                    raise ValidationError('')
            temperature = float(temperature)
            if temperature < 0 or temperature > 99.999:
                raise ValidationError('')
            return True
        except (ValueError, ValidationError) as e:
            return False

    def clean(self, *args, **kwargs):
        if not self.is_valid_format():
            raise ValidationError({'code': INVALID_HOUSE_CODE_MSG.format(self.code)})
        if self.relative_humidity != None:
            if self.relative_humidity not in VALID_RELATIVE_HUMIDITIES:
                raise ValidationError({'relative_humidity': INVALID_RELATIVE_HUMIDITY_MSG.format(self.relative_humidity)})
        if not self.temperature_is_valid(self.temperature_opentrv):
            raise ValidationError({'temperature_opentrv': INVALID_TEMPERATURE_OPENTRV_MSG.format(self.temperature_opentrv)})
        if not self.temperature_is_valid(self.temperature_ds18b20):
            raise ValidationError({'temperature_ds18b20': INVALID_TEMPERATURE_DS18B20_MSG.format(self.temperature_ds18b20)})
        if self.window != None:
            if self.window not in VALID_WINDOW_STATES:
                raise ValidationError({'window': INVALID_WINDOW_STATE_MSG.format(self.window)})
        if self.switch != None:
            if self.switch not in VALID_SWITCH_STATES:
                raise ValidationError({'switch': INVALID_SWITCH_STATE_MSG.format(self.switch)})
        if self.last_updated_all != None:
            if type(self.last_updated_all) == datetime.datetime:
                pass
            else:
                try:
                    import dateutil.parser
                    yourdate = dateutil.parser.parse(self.last_updated_all)
                except (ValueError) as e:
                    raise ValidationError({'last_updated_all': INVALID_LAST_UPDATED_ALL_MSG.format(self.last_updated_all)})
        if self.last_updated_temperature != None:
            if type(self.last_updated_temperature) == datetime.datetime:
                pass
            else:
                try:
                    import dateutil.parser
                    yourdate = dateutil.parser.parse(self.last_updated_temperature)
                except (ValueError) as e:
                    raise ValidationError({'last_updated_temperature': INVALID_LAST_UPDATED_TEMPERATURE_DATE_MSG.format(self.last_updated_temperature)})
        if self.synchronising != None:
            if self.synchronising not in VALID_SYNCHRONISING_STATES:
                raise ValidationError({'synchronising': INVALID_SYNCHRONISING_STATE_MSG.format(self.synchronising)})
        if self.ambient_light != None:
            if self.ambient_light not in VALID_AMBIENT_LIGHT_VALUES:
                raise ValidationError({'ambient_light': INVALID_AMBIENT_LIGHT_VALUE_MSG.format(self.ambient_light)})

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
    # state = models.CharField(max_length=3, default="off")
    pass

class Led(models.Model):
    colour = models.IntegerField(choices=[(i, i) for i in VALID_COLOURS])
    flash = models.IntegerField(choices=[(i, i) for i in VALID_FLASH])
