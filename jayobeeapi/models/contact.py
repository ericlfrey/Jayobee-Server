from django.db import models

class Contact(models.Model):
    user = models.ForeignKey("Seeker", on_delete=models.CASCADE)
    job = models.ForeignKey("Job", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    company = models.CharField(max_length=255)
