from django.urls import path
from . import views
from .views import index, product_categories, manufacturers, basket_detail, product_subcategories, ProductsView, \
    ProductView

urlpatterns = [
    path('basket/', basket_detail, name='basket_detail'),
    path('remove/<int:product_id>/', views.basket_remove, name='basket_remove'),
    path('basket_update_quantity/<int:product_id>/', views.basket_update_quantity, name='basket_update_quantity'),
    path('basket_add/<int:product_id>/', views.basket_add, name='basket_add'),
    path('brands/', manufacturers, name='brands'),
    path('<slug:fishing_season_slug>/<slug:category_slug>/<slug:subcategory_slug>/<slug:product_slug>/',
         ProductView.as_view(), name='product'),
    # path('<slug:fishing_season_slug>/<slug:category_slug>/<slug:subcategory_slug>/', products, name='products'),
    path('<slug:fishing_season_slug>/<slug:category_slug>/<slug:subcategory_slug>/', ProductsView.as_view(),
         name='products'),
    path('<slug:fishing_season_slug>/<slug:category_slug>/', product_subcategories, name='product_subcategories'),
    path('<slug:fishing_season_slug>/', product_categories, name='product_categories'),
    path('', index, name='index')
]
