from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('open_signup', views.open_signup, name='open_signup'),
    path('open_signin', views.open_signin, name='open_signin'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('open_add_restaurant', views.open_add_restaurant, name='open_add_restaurant'),
    path('add_restaurant', views.add_restaurant, name='add_restaurant'),
]