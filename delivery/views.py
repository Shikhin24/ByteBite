from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Item, Restaurant, User

def index(request):
    #return HttpResponse("welcome to bytebite")
    return render(request, "index.html")

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
            return HttpResponse("Username, email and password are required")
        
        if User.objects.filter(email=email).exists():
            return HttpResponse("email already exists. enter different email id")
        
        user = User(username=username, password=password, email=email, mobile=mobile, address=address)
        user.save()
        
        #return HttpResponse("sign up successful")
        #return HttpResponse(f"Username: {username}, Password: {password}, Email: {email}, mobile: {mobile}, Address: {address}")
        #return HttpResponse("Sign up successful data saved")
        
        return render(request, 'signin.html')
    
    return HttpResponse("invalid response")
    
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            return HttpResponse("Username and password are required")
        
        try:
            User.objects.get(username=username, password=password)

            if username == 'admin':
                request.session['is_admin'] = True
                return render(request, 'admin_home.html')
            else:
                request.session['is_admin'] = False
                restaurantList = Restaurant.objects.all()
                return render(request,'customer_home.html',
                    {
                        "restaurantList": restaurantList,
                        "username": username
                    }
                )  
        
        except User.DoesNotExist:
            return render(request, 'fail.html')    
        
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
    
    
        