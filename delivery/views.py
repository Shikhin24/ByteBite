import json
from django.views.decorators.cache import never_cache
from functools import wraps
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
import razorpay
from .models import AdminActivity, Cart, CartItem, Item, Restaurant, User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

def get_logged_in_user(request):
    username = request.session.get("username")
    if not username:
        return None
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        request.session.flush()
        return None


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("is_admin"):
            return redirect("/")
        return view_func(request, *args, **kwargs)
    return wrapper


def customer_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("username"):
            return redirect("/")
        return view_func(request, *args, **kwargs)
    return wrapper

@never_cache
def index(request):
    context = {
        'login_error': request.session.pop('login_error', None),
        'signup_error': request.session.pop('signup_error', None),
        'signup_success': request.session.pop('signup_success', None),
        'active_tab': request.session.pop('active_tab', 'signin'),
    }
    return render(request, "index.html", context)

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
        
        # 🔑 Password length validation
        if len(password) < 8 or len(password) > 20:
            request.session['signup_error'] = 'Password must be between 8 and 20 characters.'
            request.session['active_tab'] = 'signup'
            return redirect('/')

        if User.objects.filter(email=email).exists():
            request.session['signup_error'] = 'E-mail already exists.'
            request.session['active_tab'] = 'signup'
            return redirect('/')

        User.objects.create(
            username=username,
            password=make_password(password),
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
            user = User.objects.get(email=email)
            if not check_password(password, user.password):
                raise User.DoesNotExist

            if user.username == 'admin':
                request.session['is_admin'] = True
                return redirect('admin_home')

            request.session['is_admin'] = False
            request.session['username'] = user.username

            return redirect('customer_home')

        except User.DoesNotExist:
            request.session['login_error'] = 'Invalid e-mail or password'
            return redirect('/')
        
@never_cache
def logout_view(request):
    request.session.flush()
    response = redirect("/")
    response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"
    return response



@never_cache
@admin_required
def admin_home(request):
    if not request.session.get('is_admin'):
        return redirect('/')

    restaurant_count = Restaurant.objects.count()
    menu_count = Item.objects.count()

    context = {
        'restaurant_count': restaurant_count,
        'menu_count': menu_count,
        "activities": AdminActivity.objects.order_by("-created_at")[:5],
    }

    return render(request, 'admin_home.html', context)

@never_cache
@customer_required
def customer_home(request):
    restaurantList = Restaurant.objects.all()
    username = request.session.get('username')

    cuisines = (
        Restaurant.objects
        .values_list("cuisine", flat=True)
        .distinct()
        .order_by("cuisine")
    )
    
    ratings = (
        Restaurant.objects
        .values_list("rating", flat=True)
        .distinct()
        .order_by("-rating")
    )

    return render(
        request,
        'customer_home.html',
        {
            'restaurantList': restaurantList,
            'username': username,
            'cuisines': cuisines,
            'ratings': ratings,
        }
    )


@never_cache
@admin_required
def add_restaurant(request):
    if request.method == 'POST':
        name = request.POST.get('name').strip()
        area = request.POST.get('area', '').strip()
        picture = request.POST.get('picture')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')
        location_url = request.POST.get('location_url')

        # validation
        if not all([name, area, picture, cuisine, rating]):
            request.session['restaurant_error'] = "All fields are required."
            return redirect('admin_home')


        rating = float(rating)
        if rating < 0 or rating > 5:
            request.session['restaurant_error'] = "Rating must be between 0 and 5."
            return redirect('admin_home')


        if Restaurant.objects.filter(name__iexact=name, area__iexact=area).exists():
            request.session['restaurant_error'] = "Restaurant already exists."
            return redirect('admin_home')


        Restaurant.objects.create(
            name=name,
            area=area,
            picture=picture,
            cuisine=cuisine,
            rating=rating,
            location_url=location_url
        )

        AdminActivity.objects.create(action=f"Added restaurant: {name} ({area})")

        request.session['restaurant_success'] = "Restaurant added successfully!"
        return redirect('admin_home')


@never_cache
@admin_required      
def show_restaurant(request):
    restaurantList = Restaurant.objects.all()

    cuisines = (
        Restaurant.objects
        .values_list("cuisine", flat=True)
        .distinct()
        .order_by("cuisine")
    )

    return render(
        request,
        "show_restaurants.html",
        {
            "restaurantList": restaurantList,
            "cuisines": cuisines,
        }
    )

@never_cache
@admin_required
def open_update_menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    items = Item.objects.filter(restaurant=restaurant)

    context = {
        "restaurant": restaurant,
        "items": items,
        "menu_error": request.session.pop("menu_error", None),
        "menu_success": request.session.pop("menu_success", None),
    }

    return render(request, "update_menu.html", context)


@never_cache
@admin_required
def update_menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()
        picture = request.POST.get("picture", "").strip()
        price = request.POST.get("price", "").strip()
        nonVeg = request.POST.get("nonVeg") == "on"

        # ❌ Validation: empty fields
        if not all([name, description, picture, price]):
            request.session["menu_error"] = "All fields are required."
            return redirect("open_update_menu", restaurant_id=restaurant.id)

        # ❌ Validation: duplicate menu
        if Item.objects.filter(restaurant=restaurant, name__iexact=name).exists():
            request.session["menu_error"] = "Menu item with this name already exists."
            return redirect("open_update_menu", restaurant_id=restaurant.id)


        # ✅ Create menu
        Item.objects.create(
            restaurant=restaurant,
            name=name,
            description=description,
            picture=picture,
            price=price,
            nonVeg=nonVeg,
        )

        AdminActivity.objects.create(
            action=f"Added menu item: {name}"
        )

        request.session["menu_success"] = "Menu item added successfully!"
        return redirect("open_update_menu", restaurant_id=restaurant.id)


@never_cache
@admin_required 
def delete_menu_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    restaurant_id = item.restaurant.id
    item.delete()
    return redirect('open_update_menu', restaurant_id=restaurant_id)

@never_cache
@admin_required
def edit_menu_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    
    if request.method == 'POST':
        name = request.POST.get('name').strip()
        
        if Item.objects.filter(
            restaurant=item.restaurant,name__iexact=request.POST.get("name")).exclude(id=item.id).exists():
            request.session["menu_error"] = "Another menu item with this name already exists."
            return redirect("open_update_menu", restaurant_id=item.restaurant.id)
        
        item.name = name
        item.description = request.POST.get('description')
        item.picture = request.POST.get('picture')
        item.price = request.POST.get('price')
        item.nonVeg = request.POST.get('nonVeg') == 'on'
        item.save()

    return redirect('open_update_menu', restaurant_id=item.restaurant.id)


@never_cache
@customer_required
def view_menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    items = Item.objects.filter(restaurant=restaurant)

    cart_item_ids = []
    cart_count = 0

    if request.session.get('username'):
        user = get_logged_in_user(request)
        if not user:
            return redirect("/")

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

@never_cache
@admin_required
def update_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == 'POST':
        name = request.POST.get('name').strip()
        area = request.POST.get('area').strip()
        picture = request.POST.get('picture')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')
        location_url = request.POST.get('location_url')

        # required fields (rating checked separately)
        if not all([name, area, picture, cuisine, rating]):
            request.session["restaurant_error"] = "All fields are required."
            return redirect("show_restaurant")

        # rating validation
        try:
            rating = float(rating)
        except (TypeError, ValueError):
            request.session["restaurant_error"] = "Invalid rating value."
            return redirect("show_restaurant")

        if rating < 0 or rating > 5:
            request.session["restaurant_error"] = "Rating must be between 0 and 5."
            return redirect("show_restaurant")

        # save
        restaurant.name = name
        restaurant.area = area
        restaurant.picture = picture
        restaurant.cuisine = cuisine
        restaurant.rating = rating
        restaurant.location_url = location_url
        
        if Restaurant.objects.filter(name__iexact=name, area__iexact=area).exclude(id=restaurant.id).exists():
            request.session["restaurant_error"] = "Restaurant with this name already exists."
            return redirect("show_restaurant")

        
        restaurant.save()

        AdminActivity.objects.create(
            action=f"Updated restaurant: {name} ({area})"
        )

    return redirect("show_restaurant")

@never_cache
@admin_required
def delete_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    AdminActivity.objects.create(
        action=f"Deleted restaurant: {restaurant.name}"
    )
    restaurant.delete()
    return redirect("show_restaurant")


@never_cache
@customer_required
def add_to_cart(request, item_id):
    if request.method == 'POST':
        user = get_logged_in_user(request)
        if not user:
            return redirect("/")

        item = Item.objects.get(id=item_id)
        item_restaurant = item.restaurant

        cart, created = Cart.objects.get_or_create(customer=user)

        if not cart.cart_items.exists():
            cart.restaurant = None
            cart.save()

        
        # 🔴 Restaurant check
        if cart.restaurant and cart.restaurant != item_restaurant:
            return JsonResponse({
                'error': '❌ You cannot add items from multiple restaurants.'
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

@never_cache
@customer_required
def remove_from_cart(request, item_id):
    if request.method == 'POST':
        user = get_logged_in_user(request)
        if not user:
            return redirect("/")

        cart = Cart.objects.get(customer=user)

        CartItem.objects.filter(cart=cart, item_id=item_id).delete()

        # 🔥 CHECK IF CART IS EMPTY
        if not cart.cart_items.exists():
            cart.restaurant = None
            cart.save()

        total_qty = sum(ci.quantity for ci in cart.cart_items.all())
        total_price = cart.total_price()

        return JsonResponse({
            'total_qty': total_qty,
            'total_price': total_price
        })


@never_cache
@customer_required
def view_cart(request):
    if not settings.RAZORPAY_KEY_ID or not settings.RAZORPAY_KEY_SECRET:
        return JsonResponse({"error": "Payment disabled"}, status=503)

    if request.session.get("payment_done"):
        return redirect("customer_home")

    username = request.session['username']
    user = get_logged_in_user(request)
    if not user:
        return redirect("/")
    
    cart = Cart.objects.filter(customer=user).first()

    total_quantity = 0
    if cart:
        total_quantity = sum(ci.quantity for ci in cart.cart_items.all())

    return render(request, 'cart.html', {
        'cart': cart,
        'total_quantity': total_quantity,
        'username': username, 
        'razorpay_key': settings.RAZORPAY_KEY_ID,
    })

@never_cache
@customer_required
def update_quantity(request, item_id, action):
    if request.method == 'POST':
        user = get_logged_in_user(request)
        if not user:
            return redirect("/")

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

@never_cache
@customer_required      
def checkout(request, username):
    if not settings.RAZORPAY_KEY_ID or not settings.RAZORPAY_KEY_SECRET:
        return JsonResponse({"error": "Payment disabled"}, status=503)
    
    customer = get_logged_in_user(request)
    if not customer:
        return redirect("/")
    cart = Cart.objects.filter(customer=customer).first()

    if not cart:
        return redirect('view_cart')

    return render(request, "payment.html", {
        "total_price": cart.total_price(),
        "username": username,
        "razorpay_key": settings.RAZORPAY_KEY_ID
    })


    
razorpay_client = None
if settings.RAZORPAY_KEY_ID and settings.RAZORPAY_KEY_SECRET:
    razorpay_client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )


@csrf_exempt
def payment_success(request):
    if not settings.RAZORPAY_KEY_ID or not settings.RAZORPAY_KEY_SECRET:
        return JsonResponse({"status": "failed"}, status=503)
    
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

        request.session["payment_done"] = True
        return JsonResponse({"status": "success"})

    except Exception as e:
        return JsonResponse({"status": "failed"})
    
def cart_status(request):
    if not request.session.get('username'):
        return JsonResponse({"items": [], "total_qty": 0})

    user = get_logged_in_user(request)
    if not user:
        return redirect("/")

    cart = Cart.objects.filter(customer=user).first()

    if not cart:
        return JsonResponse({"items": [], "total_qty": 0})

    item_ids = list(cart.cart_items.values_list("item_id", flat=True))
    total_qty = sum(ci.quantity for ci in cart.cart_items.all())

    return JsonResponse({
        "items": item_ids,
        "total_qty": total_qty
    })


