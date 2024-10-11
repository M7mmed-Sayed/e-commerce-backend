from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=60, unique=True)
    description  = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.name
