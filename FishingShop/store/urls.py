from django.urls import path
from . import views
from .views import index, product_categories, manufacturers, basket_detail, product_subcategories, ProductsView, \
    ProductView, CustomerLoginView, ChangeCustomerPasswordView, RegisterCustomerView, \
    RegisterDoneView, customer_activate, DeleteCustomerAccountView, CustomerLogoutView, ResetCustomerPasswordView, \
    ResetDoneCustomerPasswordView, ResetConfirmCustomerPasswordView, ResetCompleteCustomerPasswordView
from django.views.decorators.cache import never_cache

urlpatterns = [
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/password/change/', ChangeCustomerPasswordView.as_view(), name='password_change'),
    path('accounts/profile/delete_account/', DeleteCustomerAccountView.as_view(), name='delete_account'),
    path('accounts/profile/edit_info/', views.edit_customer_profile, name='edit_customer_profile'),
    path('accounts/profile/edit_delivery/', views.edit_delivery_address_profile, name='edit_delivery_address_profile'),
    path('accounts/profile/order_tracking/<int:buy_id>/', views.order_tracking, name='order_tracking'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/register/activate/<str:sign>/', customer_activate, name='register_activate'),
    path('accounts/register/', RegisterCustomerView.as_view(), name='register'),
    path('accounts/logout/', CustomerLogoutView.as_view(), name='logout'),
    path('accounts/password_reset/complete/',
         ResetCompleteCustomerPasswordView.as_view(), name='password_reset_complete'),
    path('accounts/password_reset/<uidb64>/<token>/',
         ResetConfirmCustomerPasswordView.as_view(), name='password_reset_confirm'),
    path('accounts/password_reset/notification/',
         ResetDoneCustomerPasswordView.as_view(), name='password_reset_notification'),
    path('accounts/password_reset/',
         ResetCustomerPasswordView.as_view(), name='password_reset'),
    path('accounts/login/', CustomerLoginView.as_view(), name='login'),
    path('basket/', basket_detail, name='basket_detail'),
    path('remove/<int:product_id>/', views.basket_remove, name='basket_remove'),
    path('basket_update_quantity/<int:product_id>/', views.basket_update_quantity, name='basket_update_quantity'),
    path('basket_add/<int:product_id>/', views.basket_add, name='basket_add'),
    path('ordering/successful/', views.successful_ordering, name='successful_ordering'),
    path('ordering/', views.ordering, name='ordering'),
    path('brands/', manufacturers, name='brands'),
    path('info/<str:page>/', views.other_page, name='other'),
    path('<slug:fishing_season_slug>/<slug:category_slug>/<slug:subcategory_slug>/<slug:product_slug>/',
         ProductView.as_view(), name='product'),
    path('<slug:fishing_season_slug>/<slug:category_slug>/<slug:subcategory_slug>/',
         never_cache(ProductsView.as_view()), name='products'),
    path('<slug:fishing_season_slug>/<slug:category_slug>/', product_subcategories, name='product_subcategories'),
    path('<slug:fishing_season_slug>/', product_categories, name='product_categories'),
    path('', index, name='index')
]
