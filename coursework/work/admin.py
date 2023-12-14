from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Addresses, Status, Categories, Products, \
    Supplies, Orders, OrderItems, ProfitReport
from .views import convert_to_direct_link


# Register your models here.


# class CustomersAdmin(admin.ModelAdmin):
#     def has_add_permission(self, request, obj=None):
#         return False
#
#     def has_delete_permission(self, request, obj=None):
#         return False
#
#     list_display = (
#         'customer_lastname', 'customer_name', 'customer_surename',
#         'customer_email', 'customer_phone', 'customer_datebirth')


class AddressesAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    list_display = (
        'ad_customer', 'ad_country', 'ad_region',
        'ad_city', 'ad_street', 'ad_house', 'ad_building', 'ad_apartment',
        'ad_index')


class StatusAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    list_display = ('status_id', 'status_name')


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'category_name')


class ProductsAdmin(admin.ModelAdmin):
    list_display = (
        'prod_name', 'description', 'image_show',
        'prod_amount', 'prod_category', 'prod_sell_price', 'prod_supply_price')
    search_fields = ["prod_name"]

    def image_show(self, obj):
        r = convert_to_direct_link(obj.prod_photo)
        if r:
            return mark_safe("<img src='{}' width='60'/>".format(r))
        return "None"

    image_show.__name__ = "Картинка"


class SuppliesAdmin(admin.ModelAdmin):
    list_display = ('sup_product', 'sup_amount')


class OrdersAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    list_display = ('ord_customer', 'order_date', 'ord_status')
    list_filter = ['ord_status']


class OrderItemsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    list_display = ('oi_order', 'oi_product', 'oi_amount')


class ProfitReportsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    list_display = ('day', 'month', 'year', 'sum_profit')
    readonly_fields = ('day', 'month', 'year', 'order_id', 'sum_profit')


# admin.site.register(Customers, CustomersAdmin)
admin.site.register(Addresses, AddressesAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Supplies, SuppliesAdmin)
admin.site.register(Orders, OrdersAdmin)
admin.site.register(OrderItems, OrderItemsAdmin)
admin.site.register(ProfitReport, ProfitReportsAdmin)
