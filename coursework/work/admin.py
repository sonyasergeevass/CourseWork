from django.contrib import admin
from .models import Customer


# Register your models here.


class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'customer_id', 'customer_name', 'customer_lastname', 'customer_email',
        'customer_phone', 'customer_datebirth', 'customer_login')


admin.site.register(Customer, CustomerAdmin)
