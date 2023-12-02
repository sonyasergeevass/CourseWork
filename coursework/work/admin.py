from django.contrib import admin
from .models import Customers, Addresses, Status, Categories, Products, \
    Supplies, Orders, OrderItems


# Register your models here.


class CustomersAdmin(admin.ModelAdmin):
    list_display = (
        'customer_id', 'customer_name', 'customer_lastname', 'customer_email',
        'customer_phone', 'customer_datebirth', 'customer_login')


class AddressesAdmin(admin.ModelAdmin):
    list_display = (
        'address_id', 'ad_customer', 'ad_country', 'ad_region',
        'ad_city', 'ad_street', 'ad_house', 'ad_building', 'ad_apartment',
        'ad_index')


class StatusAdmin(admin.ModelAdmin):
    list_display = ('status_id', 'status_name')


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'category_name')


class ProductsAdmin(admin.ModelAdmin):
    list_display = (
        'product_id', 'prod_name', '__description__', 'prod_photo',
        'prod_amount', 'prod_category', 'prod_sell_price', 'prod_supply_price')


class SuppliesAdmin(admin.ModelAdmin):
    list_display = ('supply_id', 'sup_product', 'sup_amount')


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'order_date', 'ord_customer', 'ord_status')


class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('oi_order', 'oi_product', 'oi_amount')


admin.site.register(Customers, CustomersAdmin)
admin.site.register(Addresses, AddressesAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Supplies, SuppliesAdmin)
admin.site.register(Orders, OrdersAdmin)
admin.site.register(OrderItems, OrderItemsAdmin)
