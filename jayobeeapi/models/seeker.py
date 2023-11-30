from django.db import models

class Seeker(models.Model):
    uid = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
