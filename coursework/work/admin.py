from django.contrib import admin
from .models import Customers, Addresses, Status, Categories


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


admin.site.register(Customers, CustomersAdmin)
admin.site.register(Addresses, AddressesAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Categories, CategoriesAdmin)
