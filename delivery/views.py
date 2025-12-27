from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Restaurant, User

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
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')

        if not username or not password or not email:
            request.session['signup_error'] = 'All mandatory fields must be filled'
            request.session['active_tab'] = 'signup'
            return redirect('/')

        if User.objects.filter(email=email).exists():
            request.session['signup_error'] = 'Email already exists. Try another one'
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
        request.session['signup_success'] = 'Signup successful. Please sign in.'
        request.session['active_tab'] = 'signin'
        return redirect('/')
    
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            request.session['login_error'] = 'Username and password are required'
            return redirect('/')

        try:
            User.objects.get(username=username, password=password)

            if username == 'admin':
                request.session['is_admin'] = True
                return redirect('/admin_home')  # or wherever admin lands

            request.session['is_admin'] = False
            request.session['username'] = username
            return redirect('/show_restaurant')

        except User.DoesNotExist:
            request.session['login_error'] = 'Invalid username or password'
            return redirect('/')
 
        
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

    return render(request, 'view_menu.html', {'restaurant': restaurant,'items': items})

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
        