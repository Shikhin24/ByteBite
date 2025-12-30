import json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
import razorpay
from .models import Cart, CartItem, Item, Restaurant, User

def index(request):
    context = {
        'login_error': request.session.pop('login_error', None),
        'signup_error': request.session.pop('signup_error', None),
        'signup_success': request.session.pop('signup_success', None),
        'active_tab': request.session.pop('active_tab', 'signin'),
    }
    return render(request, "index.html", context)


def open_signup(request):
    return render(request, "signup.html")

def open_signin(request):
    return render(request, "signin.html")

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        email = request.POST.get('email', '').strip()
        mobile = request.POST.get('mobile', '').strip()
        address = request.POST.get('address', '').strip()

        if not username or not password or not email:
            request.session['signup_error'] = 'All fields are mandatory.'
            request.session['active_tab'] = 'signup'
            return redirect('/')

        if User.objects.filter(email=email).exists():
            request.session['signup_error'] = 'E-mail already exists.'
            request.session['active_tab'] = 'signup'
            return redirect('/')

        User.objects.create(
            username=username,
            password=password,
            email=email,
            mobile=mobile,
            address=address
        )

        # success → go to signin
        request.session['signup_success'] = 'Signup successful!'
        request.session['active_tab'] = 'signin'
        return redirect('/')
    
def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email','').strip()
        password = request.POST.get('password').strip()

        if not email or not password:
            request.session['login_error'] = 'E-mail and password are required.'
            return redirect('/')

        try:
            user = User.objects.get(email=email, password=password)

            if user.username == 'admin':
                request.session['is_admin'] = True
                return redirect('admin_home')

            request.session['is_admin'] = False
            request.session['username'] = user.username

            return redirect('customer_home')

        except User.DoesNotExist:
            request.session['login_error'] = 'Invalid e-mail or password'
            return redirect('/')
        
def admin_home(request):
    if not request.session.get('is_admin'):
        return redirect('/')

    restaurant_count = Restaurant.objects.count()
    menu_count = Item.objects.count()

    context = {
        'restaurant_count': restaurant_count,
        'menu_count': menu_count,
    }

    return render(request, 'admin_home.html', context)

def customer_home(request):
    if not request.session.get('username'):
        return redirect('/')

    restaurantList = Restaurant.objects.all()
    username = request.session.get('username')

    return render(
        request,
        'customer_home.html',
        {
            'restaurantList': restaurantList,
            'username': username
        }
    )

        
def open_add_restaurant(request):
    return render(request, 'add_restaurants.html')

def add_restaurant(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        picture = request.POST.get('picture')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')
        
        if not name or not picture or not cuisine or not rating:
            return HttpResponse("All fields are required")
        
        try:
            Restaurant.objects.get(name=name)
            return HttpResponse("Dulpicate restaurant")
        
        except:
            Restaurant.objects.create(
                name = name,
                picture = picture,
                cuisine = cuisine,
                rating = rating,
            )
        return HttpResponse("Successfully added")
        #return render(request, 'admin_home.html')
        
def show_restaurant(request):
    restaurantList = Restaurant.objects.all()
    is_admin = request.session.get('is_admin', False)

    return render(request,'show_restaurants.html',{'restaurantList': restaurantList,'is_admin': is_admin})

def open_update_menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    
    items = Item.objects.filter(restaurant=restaurant)
    return render(request,'update_menu.html',
        {'restaurant': restaurant,'items': items}
    )


def update_menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        picture = request.POST.get('picture')
        price = request.POST.get('price')
        nonVeg = request.POST.get('nonVeg') == 'on'

        if not all([name, description, picture, price]):
            return HttpResponse("All fields are required")

        if Item.objects.filter(name=name, restaurant=restaurant).exists():
            return HttpResponse("Duplicate menu")

        Item.objects.create(
            restaurant=restaurant,
            name=name,
            description=description,
            price=price,
            nonVeg=nonVeg,
            picture=picture
        )

        return HttpResponse("Menu added successfully")
    

def view_menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    items = Item.objects.filter(restaurant=restaurant)

    cart_item_ids = []
    cart_count = 0

    if request.session.get('username'):
        user = User.objects.get(username=request.session['username'])
        cart = Cart.objects.filter(customer=user).first()

        if cart:
            # IDs of items already in cart
            cart_item_ids = list(
                cart.cart_items.values_list('item_id', flat=True)
            )

            # total quantity for badge
            cart_count = sum(
                ci.quantity for ci in cart.cart_items.all()
            )

    return render(request, 'view_menu.html', {
        'restaurant': restaurant,
        'items': items,
        'cart_item_ids': cart_item_ids,
        'cart_count': cart_count
    })



def open_update_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    return render(request,'update_restaurant.html',{'restaurant': restaurant})

def update_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        picture = request.POST.get('picture')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')

        if not all([name, picture, cuisine, rating]):
            return HttpResponse("All fields are required")

        if Item.objects.filter(name=name, restaurant=restaurant).exists():
            return HttpResponse("Duplicate menu")

        restaurant.name = name
        restaurant.picture = picture
        restaurant.cuisine = cuisine
        restaurant.rating = rating

        restaurant.save()
    restaurantList = Restaurant.objects.all()
    return render(request, 'show_restaurants.html', {"restaurantList" : restaurantList})

def delete_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    restaurant.delete()
    
    restaurantList = Restaurant.objects.all()
    return render(request, 'show_restaurants.html', {"restaurantList" : restaurantList})

def add_to_cart(request, item_id):
    if request.method == 'POST':
        user = User.objects.get(username=request.session['username'])
        item = Item.objects.get(id=item_id)
        item_restaurant = item.restaurant

        cart, created = Cart.objects.get_or_create(customer=user)

        # 🔴 Restaurant check
        if cart.restaurant and cart.restaurant != item_restaurant:
            return JsonResponse({
                'error': 'You cannot add items from multiple restaurants.'
            }, status=400)

        # First item → lock restaurant
        if not cart.restaurant:
            cart.restaurant = item_restaurant
            cart.save()

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            item=item
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        cart_count = sum(ci.quantity for ci in cart.cart_items.all())

        return JsonResponse({
            'status': 'added',
            'cart_count': cart_count
        })

    
def remove_from_cart(request, item_id):
    if request.method == 'POST':
        user = User.objects.get(username=request.session['username'])
        cart = Cart.objects.get(customer=user)

        CartItem.objects.filter(cart=cart, item_id=item_id).delete()

        total_qty = sum(ci.quantity for ci in cart.cart_items.all())
        total_price = cart.total_price()

        return JsonResponse({
            'total_qty': total_qty,
            'total_price': total_price
        })


def view_cart(request):
    if not request.session.get('username'):
        return redirect('/')

    username = request.session['username']
    user = User.objects.get(username=username)
    cart = Cart.objects.filter(customer=user).first()

    total_quantity = 0
    if cart:
        total_quantity = sum(ci.quantity for ci in cart.cart_items.all())

    return render(request, 'cart.html', {
        'cart': cart,
        'total_quantity': total_quantity,
        'username': username, 
    })


def update_quantity(request, item_id, action):
    if request.method == 'POST':
        user = User.objects.get(username=request.session['username'])
        cart = Cart.objects.get(customer=user)
        cart_item = CartItem.objects.get(cart=cart, item_id=item_id)

        if action == 'inc':
            cart_item.quantity += 1
        elif action == 'dec':
            cart_item.quantity -= 1

        if cart_item.quantity <= 0:
            cart_item.delete()
        else:
            cart_item.save()

        total_qty = sum(ci.quantity for ci in cart.cart_items.all())
        total_price = cart.total_price()

        return JsonResponse({
            'quantity': cart_item.quantity if cart_item.pk else 0,
            'total_qty': total_qty,
            'total_price': total_price
        })
        
def checkout(request, username):
    customer = get_object_or_404(User, username=username)
    cart = Cart.objects.filter(customer=customer).first()

    if not cart:
        return redirect('view_cart')

    return render(request, "payment.html", {
        "total_price": cart.total_price(),
        "username": username,
        "razorpay_key": settings.RAZORPAY_KEY_ID
    })


    
razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)

@csrf_exempt
def payment_success(request):
    try:
        data = json.loads(request.body)

        # OPTIONAL: verify signature (skip if using minimal flow)
        # razorpay_client.utility.verify_payment_signature(data)

        username = request.session.get('username')
        if not username:
            return JsonResponse({"status": "failed"})

        user = User.objects.get(username=username)
        cart = Cart.objects.filter(customer=user).first()

        if cart:
            cart.cart_items.all().delete()
            cart.restaurant = None
            cart.save()

        return JsonResponse({"status": "success"})

    except Exception as e:
        return JsonResponse({"status": "failed"})





