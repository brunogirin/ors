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
    temperature_opentrv = models.CharField(max_length=6, default=None, null=True, blank=True)
    ds18b20_temperature = models.CharField(max_length=6, default=None, null=True, blank=True)
    button = models.CharField(max_length=3, default="off", choices=[(i, i) for i in ["off", "on"]])
    led = models.IntegerField(choices=[(i, i) for i in range(4)], default=0)
    synchronising = models.CharField(max_length=3, default="off", choices=[(i, i) for i in ["off", "on"]])
    relative_humidity = models.IntegerField(choices=[(i, i) for i in range(101)], default=0)
    window = models.CharField(max_length=6, choices=[(i, i) for i in ["open", "closed"]], default="closed")
    last_updated = models.DateTimeField(default=None, null=True, blank=True)
    last_updated_temperatures = models.DateTimeField(default=None, null=True, blank=True)

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

class Debug(models.Model):
    state = models.CharField(max_length=3, default="off")

class Led(models.Model):
    colour = models.IntegerField(choices=[(i, i) for i in VALID_COLOURS])
    flash = models.IntegerField(choices=[(i, i) for i in VALID_FLASH])
