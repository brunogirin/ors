from django.db import models

# Create your models here.
class Debug(models.Model):
    state = models.CharField(max_length=3, default="off")
