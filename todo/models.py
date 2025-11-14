from django.db import models

class Todo(models.Model):
    person = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='todos/', null=True, blank=True)
    status = models.CharField(max_length=50)
    start_data = models.DateTimeField()
    finish_data = models.DateTimeField()
