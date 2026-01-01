from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length = 20)
    password = models.CharField(max_length = 8)
    email = models.EmailField(max_length = 20, unique=True)
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
    
class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def total_price(self):
        return sum(ci.item.price * ci.quantity for ci in self.cart_items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        related_name="cart_items",
        on_delete=models.CASCADE
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'item')

class AdminActivity(models.Model):
    action = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.action
