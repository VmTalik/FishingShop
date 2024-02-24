from django.contrib import admin
from .models import (Product, AdditionalProductImage, Warehouse, Manufacturer, Category, SubCategory, FishingSeason,
                     Step, Comment, ProductParameter, ProductParameterValue, ProductParameterValueStr, Customer, Buy,
                     BuyStep)


class ProductParameterValueInline(admin.StackedInline):
    model = ProductParameterValue


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductParameterValueInline]
    search_fields = ('name', 'subcategory__subcategory_name', 'subcategory__category__category_name')
    prepopulated_fields = {'slug': ('name',)}


class BuyStepAdminInline(admin.StackedInline):
    model = BuyStep


class BuyAdmin(admin.ModelAdmin):
    inlines = [BuyStepAdminInline]
    search_fields = ('customer__username',)
    ordering = ['-buystep__step_begin_datetime']


admin.site.register([AdditionalProductImage,
                     Warehouse,
                     Manufacturer,
                     Category,
                     SubCategory,
                     FishingSeason,
                     Step,
                     Comment,
                     ProductParameter,
                     ProductParameterValueStr,
                     Customer])
admin.site.register(Product, ProductAdmin)
admin.site.register(Buy, BuyAdmin)
