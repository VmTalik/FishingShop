from django.urls import path, include
from . import views
from .views import index, product_categories, manufacturers, basket_detail, product_subcategories, ProductsView, \
    ProductView

urlpatterns = [
    path('remove/<int:product_id>/', views.basket_remove, name='basket_remove'),
    path('basket_update_quantity/<int:rod_id>/', views.basket_update_quantity, name='basket_update_quantity'),
    path('basket_add/<int:rod_id>/', views.basket_add, name='basket_add'),
    # path('<slug:fishing_season_slug>/<slug:category_slug>/<slug:subcategory_slug>/<int:rod_id>/', product, name='rod'),
    # path('<slug:fishing_season_slug>/<slug:category_slug>/<slug:subcategory_slug>/<slug:product_slug>/',
    #    product, name='product'),
    path('<slug:fishing_season_slug>/<slug:category_slug>/<slug:subcategory_slug>/<slug:product_slug>/',
         ProductView.as_view(), name='product'),
    # path('<slug:fishing_season_slug>/<slug:category_slug>/<slug:subcategory_slug>/', products, name='products'),
    path('<slug:fishing_season_slug>/<slug:category_slug>/<slug:subcategory_slug>/', ProductsView.as_view(),
         name='products'),
    path('<slug:fishing_season_slug>/<slug:category_slug>/', product_subcategories, name='product_subcategories'),
    path('<slug:fishing_season_slug>/', product_categories, name='product_categories'),

    path('basket', basket_detail, name='basket_detail'),
    path('brands', manufacturers, name='brands'),
    path('', index, name='index')
]

