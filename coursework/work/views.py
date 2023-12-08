from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Products, Categories


# def welcome(request):
#     return render(request, 'main.html')
def convert_to_direct_link(gdrive_url):
    file_id = gdrive_url.split('/d/')[1].split('/view')[0]
    return f'https://drive.google.com/uc?id={file_id}'


def categories_list():
    return Categories.objects.all()


def product_list(request):
    search_query = request.GET.get('q', '')
    if search_query:
        products = Products.objects.filter(name__icontains=search_query)
    else:
        products = Products.objects.all()
    for product in products:
        if product.prod_photo:
            product.prod_photo = convert_to_direct_link(product.prod_photo)
    categories = categories_list()
    return render(request, 'show_products.html',
                  {'products': products, 'categories': categories})


def login_page(request):
    if request.method == 'POST':
        customer_email = request.POST.get('customer_email')
        customer_password = request.POST.get('customer_password')

        user = authenticate(request, username=customer_email,
                            password=customer_password)

        if user:
            login(request, user)
            return redirect('welcome')
        else:
            messages.error(request, 'Неверно')

    return render(request, 'login.html')


def search_products(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')
        results = Products.objects.filter(prod_name__icontains=query)
        return render(request, 'search_results.html',
                      {'results': results})
