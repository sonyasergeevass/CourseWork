from django.shortcuts import render, get_object_or_404
from .models import Products, Categories, Orders, OrderItems
from cart.forms import CartAddProductForm


def product_detail(request, product_id):
    product = get_object_or_404(Products, pk=product_id)
    cart_product_form = CartAddProductForm()
    if product.prod_photo:
        product.prod_photo = convert_to_direct_link(product.prod_photo)
    return render(request, 'product_detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})


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
    if gdrive_url:
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


def user_orders(request):
    current_user = request.user
    orders = Orders.objects.filter(ord_customer=current_user).exclude(
        ord_status__status_name='Временный').order_by('-order_date')

    orders_data = []

    for order in orders:
        order_items = OrderItems.objects.filter(oi_order=order)
        items_data = []
        full_price = 0
        for item in order_items:
            items_data.append({
                'product_name': item.oi_product.prod_name,
                # Замените на поле, которое содержит название товара
                'prod_photo': convert_to_direct_link(
                    item.oi_product.prod_photo),
                'price': item.oi_product.prod_sell_price,
                'total_price': item.oi_product.prod_sell_price*item.oi_amount,
                'amount': item.oi_amount
            })
            full_price += item.oi_product.prod_sell_price*item.oi_amount
        orders_data.append({
            'order_id': order.order_id,
            'order_date': order.order_date,
            # 'customer': order.ord_customer.username,
            # Замените на поле, которое содержит информацию о покупателе
            'status': order.ord_status.status_name,
            # Замените на поле, которое содержит название статуса заказа
            'items': items_data,
            'full_price': full_price
        })
    return render(request, 'user_orders.html', {'orders_data': orders_data})


def search_products(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')
        results = Products.objects.filter(prod_name__icontains=query)
        return render(request, 'search_results.html',
                      {'results': results})
