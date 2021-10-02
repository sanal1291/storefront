from django.contrib import admin
from django.db.models.query import QuerySet
from django.utils.html import format_html, urlencode
from django.urls import reverse
from django.db.models.aggregates import Count
from django.http.request import HttpRequest
from . import models
# Register your models here.


class InventoryFilter(admin.SimpleListFilter):
    title = "inventory"
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<200', 'low')
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<200':
            return queryset.filter(inventory__lt=200)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price',
                    'inventory_stats', 'collection_title']
    list_editable = ['unit_price']
    list_per_page = 25
    list_select_related = ['collection']
    list_filter = ['collection', 'last_update', InventoryFilter]

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_stats(self, product):
        if product.inventory < 400:
            return 'low'
        return 'Ok'


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'payment', 'placed_at']
    list_per_page = 25
    list_select_related = ['customer']
    ordering = ['id']


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']

    @admin.display(ordering="products_count")
    def products_count(self, collection):
        url = (reverse('admin:store_product_changelist') +  # admin:app_model_page
               '?' +
               urlencode({'collection_id': str(collection.id)})
               )
        return format_html("<a href={}>{}</a>", url, collection.products_count)

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'order_count']
    list_editable = ['membership']
    list_per_page = 25
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='order_count')
    def order_count(self, customer):
        url = (reverse('admin:store_order_changelist') +
               '?' +
               urlencode({'customer_id': str(customer.id)})
               )
        return format_html("<a href='{}'>{}</a>", url, customer.order_count)

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).annotate(
            order_count=Count('order')
        )
