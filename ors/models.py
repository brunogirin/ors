from django.db import models

class HouseCode(models.Model):
    code = models.CharField(max_length=50)
