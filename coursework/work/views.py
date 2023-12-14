from django.shortcuts import render, get_object_or_404
from .models import Products, Categories


def product_detail(request, product_id):
    product = get_object_or_404(Products, pk=product_id)
    if product.prod_photo:
        product.prod_photo = convert_to_direct_link(product.prod_photo)
    return render(request, 'product_detail.html', {'product': product})


def category_products(request, category_id):
    categories = categories_list()
    category = get_object_or_404(Categories, pk=category_id)
    products = Products.objects.filter(prod_category=category)
    for product in products:
        if product.prod_photo:
            product.prod_photo = convert_to_direct_link(product.prod_photo)
    return render(request, 'category_products.html',
                  {'category': category, 'products': products,
                   'categories': categories})


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


def search_products(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')
        results = Products.objects.filter(prod_name__icontains=query)
        return render(request, 'search_results.html',
                      {'results': results})
