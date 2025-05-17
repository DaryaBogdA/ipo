from django.shortcuts import render

def index(request):
    return render(request, 'main/home.html')

def about_i(request):
    return render(request, 'main/about_i.html')

def about_shop(request):
    return render(request, 'main/about_shop.html')
