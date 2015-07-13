from django.db import models

class HouseCode(models.Model):
    code = models.CharField(primary_key=True, max_length=50)
