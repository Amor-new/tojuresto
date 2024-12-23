from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.sessions.models import Session



# Create your views here.
# from django.shortcuts import render

# def home(request):
#     return render(request, 'home.html')

# def about(request):
#     return render(request, 'about.html')

# def recipes(request):
#     return render(request, 'recipes.html')

# def contact(request):
#     return render(request, 'contact.html')

def index(request):
    return render(request, 'index.html')

def order(request):
    from .models import Product  # Import within the function
    products = Product.objects.all()
    return render(request, 'order.html', {'products': products})

def base(request):
    return render(request, 'base.html')

def product(request,pk):
    from .models import Product
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})
