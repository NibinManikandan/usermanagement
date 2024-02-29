from django.db import models


# Create your models here.
class CustomUser(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=25)
    password = models.CharField(max_length=20)
    def __str__(self):
        return self.name