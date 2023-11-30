from django.db import models

class Offer(models.Model):
    job = models.ForeignKey("Job", on_delete=models.CASCADE)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    amount = models.FloatField()
    benefits = models.TextField()
