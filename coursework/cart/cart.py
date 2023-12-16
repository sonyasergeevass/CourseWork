from django.shortcuts import get_object_or_404
from work.models import Products, Orders, OrderItems, Status
from decimal import Decimal


class Cart(object):

    def __init__(self, user):
        self.user = user

    def add(self, product_id, quantity=1):
        """
                Добавить продукт в корзину или обновить его количество.
                """
        status_temporary = Status.objects.get(status_name='Временный')
        order, created = Orders.objects.get_or_create(
            ord_customer=self.user,
            ord_status=status_temporary
        )

        product = get_object_or_404(Products, product_id=product_id)

        order_item, created = OrderItems.objects.get_or_create(
            oi_order=order,
            oi_product=product,
            defaults={'oi_amount': quantity}
        )

        if not created:
            order_item.oi_amount += quantity
            order_item.save()

    def remove(self, product):
        """
        Удаление товара из корзины.
        """
        OrderItems.objects.filter(oi_order__ord_customer=self.user,
                                  oi_product=product).delete()

    def get_items(self):
        """
        Получить все элементы заказа для пользователя.
        """
        return OrderItems.objects.filter(
            oi_order__ord_customer=self.user,
            oi_order__ord_status__status_name='Временный')

    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        items = self.get_items()
        return sum(
            item.oi_product.prod_sell_price * item.oi_amount for item in items)

    def get_total_price_for_item(self, item):
        """
        Подсчет общей цены для конкретного товара в корзине.
        """
        return Decimal(item.oi_product.prod_sell_price) * item.oi_amount

    def place_order(self):
        # Get the "Awaiting Payment" status
        awaiting_payment_status = Status.objects.get(
            status_name='Ожидает оплаты')

        # Update the status of order items in the cart
        order = Orders.objects.get(ord_customer=self.user,
                                   ord_status__status_name="Временный")
        order.ord_status = awaiting_payment_status
        print(f'{order.ord_status}, {order.order_id}')
        order.save()
# class Cart(object):
#
#     def __init__(self, request):
#         """
#         Инициализируем корзину
#         """
#         self.session = request.session
#         cart = self.session.get(settings.CART_SESSION_ID)
#         if not cart:
#             # save an empty cart in the session
#             cart = self.session[settings.CART_SESSION_ID] = {}
#         self.cart = cart
#
#     def add(self, product, quantity=1, update_quantity=False):
#         """
#         Добавить продукт в корзину или обновить его количество.
#         """
#         product_id = str(product.product_id)
#         if product_id not in self.cart:
#             self.cart[product_id] = {'quantity': 0,
#                                      'price': str(product.prod_sell_price),
#                                      'photo': convert_to_direct_link(
#                                          product.prod_photo)}
#         if update_quantity:
#             self.cart[product_id]['quantity'] = quantity
#         else:
#             self.cart[product_id]['quantity'] += quantity
#         self.save()
#
#     def save(self):
#         # Обновление сессии cart
#         self.session[settings.CART_SESSION_ID] = self.cart
#         # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
#         self.session.modified = True
#
#     def remove(self, product):
#         """
#         Удаление товара из корзины.
#         """
#         product_id = str(product.product_id)
#         if product_id in self.cart:
#             del self.cart[product_id]
#             self.save()
#
#     def __iter__(self):
#         """
#         Перебор элементов в корзине и получение продуктов из базы данных.
#         """
#         product_ids = self.cart.keys()
#         # получение объектов product и добавление их в корзину
#         products = Products.objects.filter(product_id__in=product_ids)
#         for product in products:
#             self.cart[str(product.product_id)]['product'] = product.to_json()
#
#         for item in self.cart.values():
#             item['total_price'] = str(
#                 Decimal(item['price']) * item['quantity'])
#             yield item
#
#     def __len__(self):
#         """
#         Подсчет всех товаров в корзине.
#         """
#         return sum(item['quantity'] for item in self.cart.values())
#
#     def get_total_price(self):
#         """
#         Подсчет стоимости товаров в корзине.
#         """
#         return sum(Decimal(item['price']) * item['quantity'] for item in
#                    self.cart.values())
#
#     def clear(self):
#         # удаление корзины из сессии
#         del self.session[settings.CART_SESSION_ID]
#         self.session.modified = True
