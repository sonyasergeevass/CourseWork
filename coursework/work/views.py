from django.shortcuts import render
from .models import Products, Categories


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
