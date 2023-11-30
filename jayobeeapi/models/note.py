from django.db import models

class Note(models.Model):
    job = models.ForeignKey("Job", on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    noteBody = models.TextField()
