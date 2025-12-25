from django.contrib import admin
from .models import Item, User, Restaurant

# Register your models here.
admin.site.register(User)
admin.site.register(Restaurant)
admin.site.register(Item)