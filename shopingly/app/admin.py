from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name',
                    'locality', 'city', 'zipcode', 'provience']


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price', 'discounted_price',
                    'description', 'brand', 'category', 'product_image']


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity']


@admin.register(OrderPlaced)
class OrderplacedModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'customer', 'product',
                    'quantity', 'ordered_date', 'status']
