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
    
class Restaurant(models.Model):
    name = models.CharField(max_length=100, unique=True)
    picture = models.URLField()
    cuisine = models.CharField(max_length=200)
    rating = models.FloatField()
    
    def __str__(self):
        return self.name
    
class Item(models.Model):
    restaurant =  models.ForeignKey(Restaurant, on_delete= models.CASCADE, related_name="items")
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    price = models.FloatField()
    nonVeg = models.BooleanField(default=False)
    picture = models.URLField()
    
    def __str__(self):
        return self.name