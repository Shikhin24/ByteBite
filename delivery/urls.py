from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name="index"),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path("logout/", views.logout_view, name="logout"),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('customer/', views.customer_home, name='customer_home'),
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
    path('menu/delete/<int:item_id>/', views.delete_menu_item, name='delete_menu_item'),
path('menu/edit/<int:item_id>/', views.edit_menu_item, name='edit_menu_item'),

    path('restaurant/<int:restaurant_id>/view_menu/',
    views.view_menu,
    name='view_menu'
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
    path('checkout/', views.checkout, name='checkout'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path("cart/status/", views.cart_status, name="cart_status"),

]
handler404 = "django.views.defaults.page_not_found"
handler500 = "django.views.defaults.server_error"
