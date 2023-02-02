from django.contrib import admin
from django.contrib.auth import get_user_model

from shop_service.models import Product, Category, Order

admin.site.register(get_user_model())


admin.site.register(Category)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ("category__name",)


admin.site.register(Order)
