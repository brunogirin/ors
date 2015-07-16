from django.db import models
VALID_COLOURS = range(4)
VALID_FLASH = [1, 2, 4, 8, 16]

# Create your models here.
class HouseCode(models.Model):
    code = models.CharField(primary_key=True, max_length=50)

class Debug(models.Model):
    state = models.CharField(max_length=3, default="off")

class Led(models.Model):
    colour = models.IntegerField(choices=[(i, i) for i in VALID_COLOURS])
    flash = models.IntegerField(choices=[(i, i) for i in VALID_FLASH])
