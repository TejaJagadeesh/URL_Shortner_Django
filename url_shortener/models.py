from django.db import models

# Create your models here.
class URL(models.Model):
    orignal_url=models.URLField()
    short_url=models.CharField(max_length=100)