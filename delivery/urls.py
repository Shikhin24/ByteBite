from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('open_signup', views.open_signup, name='open_signup'),
    path('open_signin', views.open_signin, name='open_signin'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('customer/', views.customer_home, name='customer_home'),
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
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('update-quantity/<int:item_id>/<str:action>/', views.update_quantity, name='update_quantity'),

    
]