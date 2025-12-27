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
    path('show_restaurant', views.show_restaurant, name='show_restaurant'),
    path('restaurant/<int:restaurant_id>/open_update_menu/',
        views.open_update_menu,
        name='open_update_menu'
    ),

    path('restaurant/<int:restaurant_id>/update_menu/',
        views.update_menu,
        name='update_menu'
    ),
    path('restaurant/<int:restaurant_id>/view_menu/',
    views.view_menu,
    name='view_menu'
    ),
    path('restaurant/<int:restaurant_id>/open_update_restaurant/',
        views.open_update_restaurant,
        name='open_update_restaurant'
    ),
    path('restaurant/<int:restaurant_id>/update_restaurant/',
        views.update_restaurant,
        name='update_restaurant'
    ),
    path('restaurant/<int:restaurant_id>/delete_restaurant/',
        views.delete_restaurant,
        name='delete_restaurant'
    ),
    
]