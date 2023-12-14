from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from work.models import Products
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Products, product_id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
        # request.session['added_product'] = {'prod_photo': converted_photo}
        # print(f"{type(request.session['added_product'].get('prod_photo'))}")
        print(
            f"Product {product.prod_name} added to the cart with quantity "
            f"{cd['quantity']}.")
        print(f"Cart contents: {cart.cart}")
    # else:
    #     print("Form is not valid.")
    #     print(form.errors)
    # session_data = dict(request.session)
    # print(f"{session_data}")
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Products, product_id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    # converted_photo = convert_to_direct_link(product.prod_photo)
    return render(request, 'cart/detail.html',
                  {'cart': cart})
