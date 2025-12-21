from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length = 20)
    password = models.CharField(max_length = 8)
    email = models.CharField(max_length = 20)
    mobile = models.CharField(max_length = 10)
    address = models.CharField(max_length = 50)
    
    def __str__(self):
        return self.username