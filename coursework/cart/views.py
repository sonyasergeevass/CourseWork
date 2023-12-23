from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from work.models import Products
from .cart import Cart
from .forms import CartAddProductForm


def convert_to_direct_link(gdrive_url):
    if gdrive_url:
        file_id = gdrive_url.split('/d/')[1].split('/view')[0]
        return f'https://drive.google.com/uc?id={file_id}'


@require_POST
def cart_add(request, product_id):
    cart = Cart(request.user, request)
    product = get_object_or_404(Products, pk=product_id)
    max_quantity_value = product.prod_amount
    form = CartAddProductForm(max_quantity1=max_quantity_value,
                              data=request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product_id=product_id, quantity=cd['quantity'])

    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request.user, request)
    product = get_object_or_404(Products, product_id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request.user, request)
    cart_items = cart.get_items()
    total_price = cart.get_total_price()

    processed_cart_items = []
    out_of_stock_items = []
    for item in cart_items:
        total_price_for_item = cart.get_total_price_for_item(item)
        processed_item = {
            'oi_prod_name': item.oi_product,
            'oi_product_id': item.oi_product_id,
            'oi_amount': item.oi_amount,
            'photo_url': convert_to_direct_link(item.oi_product.prod_photo),
            'total_price_for_item': total_price_for_item

        }
        if item.oi_amount > 0 and item.oi_product.prod_amount > 0:
            processed_cart_items.append(processed_item)
        elif item.oi_amount == 0 and item.oi_product.prod_amount == 0:
            out_of_stock_items.append(processed_item)
        elif item.oi_amount == 0 and item.oi_product.prod_amount > 0:
            item.oi_amount = 1
            item.save()
            processed_item['oi_amount'] = item.oi_amount
            processed_item[
                'total_price_for_item'] = cart.get_total_price_for_item(item)
            processed_cart_items.append(processed_item)
        elif item.oi_amount > 0 and item.oi_product.prod_amount == 0:
            processed_cart_items.append(processed_item)

    total_price = cart.get_total_price()
    context = {
        'cart_items': processed_cart_items,
        'out_of_stock_items': out_of_stock_items,
        'total_price': total_price,
    }

    return render(request, 'cart/detail.html', context)


def cart_place_order(request):
    if request.method == 'POST' and 'place_order' in request.POST:
        cart = Cart(request.user, request)
        print(f'CAAAAAAAAAAAAART{cart}')
        try:
            cart.place_order()
            messages.success(request, 'Заказ создан. Спасибо!')
        except ValueError as e:
            messages.error(request, str(e))
            # Добавляем сообщение об ошибке в случае нехватки товара

        # return render(request, 'user_orders.html',
        #               {'success': messages.success})
        return redirect(
            'cart:cart_detail')
    else:
        # Handle non-POST requests or requests without 'place_order'
        # You might want to redirect to a different page or show an error
        # message
        return redirect(
            'cart:cart_detail')  # Redirect to the cart detail page or any
        # other page
# def cart_detail(request):
#     cart = Cart(request)
#     # converted_photo = convert_to_direct_link(product.prod_photo)
#     return render(request, 'cart/detail.html',
#                   {'cart': cart})
# @require_POST
# def cart_add(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Products, product_id=product_id)
#     form = CartAddProductForm(request.POST)
#     if form.is_valid():
#         cd = form.cleaned_data
#         cart.add(product=product,
#                  quantity=cd['quantity'],
#                  update_quantity=cd['update'])
#
#         with (transaction.atomic()):
#             order = Orders.objects.filter(
#                 ord_customer=request.user,
#                 ord_status__status_name='Временный').first()
#             if not order:
#                 order = Orders.objects.create(ord_customer=request.user,
#                                               ord_status=Status.objects.get(
#                                                   status_name='Временный'))
#         for item in cart:
#             product = Products.objects.get(
#                 product_id=item['product']['product_id'])
#             order_item, created = OrderItems.objects.get_or_create(
#                 oi_order=order,
#                 oi_product=product,
#                 defaults={'oi_amount': item['quantity']}
#             )
#             if not created:
#                 order_item.oi_amount += item['quantity']
#                 order_item.save()
#
#         # request.session['added_product'] = {'prod_photo': converted_photo}
#         # print(f"{type(request.session['added_product'].get(
#         'prod_photo'))}")
#         # print(
#         #     f"Product {product.prod_name} added to the cart with quantity "
#         #     f"{cd['quantity']}.")
#         # print(f"Cart contents: {cart.cart}")
#     # else:
#     #     print("Form is not valid.")
#     #     print(form.errors)
#     # session_data = dict(request.session)
#     # print(f"{session_data}")
#     return redirect('cart:cart_detail')
#
#
# def cart_remove(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Products, product_id=product_id)
#     cart.remove(product)
#     return redirect('cart:cart_detail')
#
#
# def cart_detail(request):
#     cart = Cart(request)
#     # converted_photo = convert_to_direct_link(product.prod_photo)
#     return render(request, 'cart/detail.html',
#                   {'cart': cart})
