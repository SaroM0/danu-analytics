from django.shortcuts import render

def home(request):
    return render(request, 'analytics/home.html')

def chatbot(request):
    return render(request, 'analytics/chatbot.html')

def map(request):
    return render(request, 'analytics/map.html')

def predictions(request):
    return render(request, 'analytics/predictions.html')

def products(request):
    return render(request, 'analytics/products.html')

def stores(request):
    return render(request, 'analytics/stores.html')