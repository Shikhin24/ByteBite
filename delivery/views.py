from django.http import HttpResponse
from django.shortcuts import render
from .models import Restaurant, User

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
            User.objects.get(username = username, password = password)
            if username == 'admin':
                return render(request, 'admin_home.html')
            else:
                return render(request, 'customer_home.html')   
        
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
    
        