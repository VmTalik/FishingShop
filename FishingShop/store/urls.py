from django.urls import path
from .views import index, catalog_summer, manufacturers, rod_type, rods, rod

urlpatterns = [
    path('catalog-summer/rod_type/<int:rod_type_id>/<int:rod_id>/', rod, name='rod'),
    path('catalog-summer/rod_type/<int:rod_type_id>/', rods, name='rods'),
    path('catalog-summer/rod_type', rod_type, name='rod_type'),
    path('catalog-summer', catalog_summer, name='catalog-summer'),
    path('brands', manufacturers, name='brands'),
    path('', index, name='index')
]