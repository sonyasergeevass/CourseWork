from django.shortcuts import render
from .models import Products


# def welcome(request):
#     return render(request, 'main.html')


def product_list(request):
    products = Products.objects.all()
    return render(request, 'show_products.html',
                  {'products': products})
