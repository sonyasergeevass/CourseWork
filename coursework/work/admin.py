from django.contrib import admin
from django.db.models import Sum, DateTimeField, Count
from django.db.models.functions import Trunc
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
    list_editable = ["prod_amount", "prod_sell_price", "prod_supply_price"]

    def image_show(self, obj):
        r = convert_to_direct_link(obj.prod_photo)
        if r:
            return mark_safe("<img src='{}' width='60'/>".format(r))
        return "None"

    image_show.__name__ = "Картинка"


class SuppliesAdmin(admin.ModelAdmin):
    list_display = ('sup_product', 'sup_amount')


class OrderItemsInline(admin.TabularInline):
    # def has_add_permission(self, request, obj=None):
    #     return False
    #
    # def has_delete_permission(self, request, obj=None):
    #     return False

    model = OrderItems
    list_display = ('oi_order', 'oi_product', 'oi_amount')


class OrdersAdmin(admin.ModelAdmin):
    # def has_add_permission(self, request, obj=None):
    #     return False
    #
    # def has_delete_permission(self, request, obj=None):
    #     return False

    list_display = ('ord_customer', 'order_date', 'ord_status')
    list_filter = ['ord_status']
    inlines = [OrderItemsInline]


def get_next_in_date_hierarchy(request, date_hierarchy):
    if date_hierarchy + '__day' in request.GET:
        return 'minute'

    if date_hierarchy + '__month' in request.GET:
        return 'day'

    if date_hierarchy + '__year' in request.GET:
        return 'week'

    return 'week'


class ProfitReportsAdmin(admin.ModelAdmin):
    # def has_add_permission(self, request):
    #     return False
    #
    # def has_delete_permission(self, request, obj=None):
    #     return False
    #
    # list_display = ('day', 'month', 'year', 'sum_profit')
    # readonly_fields = ('day', 'month', 'year', 'order_id', 'sum_profit')

    change_list_template = 'admin/profit_report_list.html'
    date_hierarchy = 'order_date'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
            'total': Count('order_id'),
            'sum_profit': Sum('sum_profit'),
        }
        summary = list(
            qs
            .values('order_date')
            .annotate(**metrics)
            .order_by('-sum_profit')
        )
        response.context_data['summary'] = summary
        response.context_data['summary_total'] = dict(
            qs.aggregate(**metrics))

        period = get_next_in_date_hierarchy(request, self.date_hierarchy)
        response.context_data['period'] = period

        summary_over_time = qs.annotate(
            period=Trunc(
                'order_date',
                period,
                output_field=DateTimeField(),
            ),
        ).values('period').annotate(total=Sum('sum_profit')).order_by('period')

        response.context_data['summary_over_time'] = [{
            'period': x['period'],
            'total': x['total'] or 0,
            'percent_of_total': format(
                ((x['total'] or 0) / response.context_data['summary_total'][
                    'sum_profit']) * 100
                if response.context_data['summary_total'][
                       'sum_profit'] != 0 else 0,
                '.2f'),
        } for x in summary_over_time]

        return response


# admin.site.register(Customers, CustomersAdmin)
admin.site.register(Addresses, AddressesAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Supplies, SuppliesAdmin)
admin.site.register(Orders, OrdersAdmin)
# admin.site.register(OrderItems, OrderItemsAdmin)
admin.site.register(ProfitReport, ProfitReportsAdmin)
