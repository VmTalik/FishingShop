from store.models import Manufacturer, FishingSeason, Product, ProductParameterValue, Category, SubCategory, Customer, \
    Step, BuyStep, BuyProduct, Buy
from store.serializers import ManufacturerSerializer, SubCategorySerializer, ProductSerializer
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views.decorators.http import require_POST
from .basket import Basket
from .forms import BasketAddProductForm, CustomerForm, ChangeCustomerInfoForm, RegisterCustomerForm, BuyForm, \
    CustomerBuyForm, CustomerProfileDeliveryForm, CustomerProfileForm
import sys
from pympler.asizeof import asizeof
import time
from django.views.generic.detail import DetailView
from django.http import Http404
from django.views.generic import ListView, DetailView
from django.db.models import Prefetch
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.base import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.core.signing import BadSignature
from .utilities import signer


def index(request):
    return render(request, 'store/index.html')

def manufacturers(request):
    manufacturers_queryset = Manufacturer.objects.all()
    context = {'manufacturers_queryset': manufacturers_queryset}
    return render(request, 'store/manufacturers.html', context)


"""
class ManufacturersView(ListView):
    model = Manufacturer
    template_name = 'store/manufacturers.html'
    context_object_name = 'manufacturers_queryset'
"""


# вместо catalog назвал fishing_season_catalog это по сути категории товаров category
def product_categories(request, fishing_season_slug):
    # каталог категорий товаров в зависимости от рыболовного сезона
    product_categories_queryset = (
        (Category.objects.filter(fishing_season__fishing_season_slug=fishing_season_slug)
         .select_related('fishing_season')))
    # first_product_category = product_categories_queryset[0]
    context = {'product_categories_queryset': product_categories_queryset,
               }
    if product_categories_queryset:
        return render(request, 'store/product_categories.html', context)
    else:
        raise Http404('Нет такой страницы с категориями товаров!')


def product_subcategories(request, fishing_season_slug, category_slug):
    # подкатегории товаров
    product_subcategories_queryset = (
        SubCategory.objects.filter(category__category_slug=category_slug,
                                   category__fishing_season__fishing_season_slug=fishing_season_slug)
        .select_related('category')
        .select_related('category__fishing_season'))
    # first_product_subcategory = product_subcategories_queryset[0]
    context = {'product_subcategories_queryset': product_subcategories_queryset
               }
    if product_subcategories_queryset:
        return render(request, 'store/product_subcategories.html', context)
    else:
        raise Http404('Нет такой страницы с подкатегориями товаров!')


"""
def products(request, fishing_season_slug, category_slug, subcategory_slug):
    current_products_queryset = (Product.objects.filter(
        subcategory__subcategory_slug=subcategory_slug,
        subcategory__category__category_slug=category_slug,
        subcategory__category__fishing_season__fishing_season_slug=fishing_season_slug)
                                 .prefetch_related('productparametervalue_set')
                                 )
    print(current_products_queryset.query)
    # for product in current_products_queryset
    # current_manufacturer_names.add(current_rod.rod_manufacturer_id.manufacturer_name)
    context = {'current_products_queryset': current_products_queryset}
    if current_products_queryset:
        return render(request, 'store/products.html', context)
    else:
        raise Http404('Нет такой страницы с товарами!')
"""


class ProductsView(ListView):
    template_name = 'store/products.html'
    context_object_name = 'current_products_queryset'
    allow_empty = False

    def get_queryset(self):
        return (Product.objects.filter(
            subcategory__subcategory_slug=self.kwargs['subcategory_slug'],
            subcategory__category__category_slug=self.kwargs['category_slug'],
            subcategory__category__fishing_season__fishing_season_slug=self.kwargs['fishing_season_slug'])
                .select_related('subcategory__category__fishing_season')
                .select_related('manufacturer')
                .prefetch_related(Prefetch('productparametervalue_set',
                                           queryset=ProductParameterValue.objects.all()
                                           .select_related('product_param', 'product_param_value_str')))
                # .prefetch_related('productparametervalue_set')
                # .prefetch_related('productparametervalue_set__product_param_value_str')
                # .prefetch_related('productparametervalue_set__product_param')
                )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start_time = time.time()
        context['current_manufacturers'] = {i.manufacturer.manufacturer_name for i in
                                            context['current_products_queryset']}
        end_time = time.time()
        elapsed_time = end_time - start_time
        print('Elapsed time1:', elapsed_time)
        """
        start_time = time.time()
        context['product_param_str'], context['product_param_int'] = [], []
        for i in context['current_products_queryset'][0].productparametervalue_set.all():
            if i.product_param_value_str:
                context['product_param_str'].append(i)
            else:
                context['product_param_int'].append(i)

        end_time = time.time()
        elapsed_time = end_time - start_time
        print('Elapsed time2:', elapsed_time)
        """
        # params_int_dict = {}
        """
        start_time = time.time()
        context['product_param_str'], context['product_param_int'] = [], []
        for product in context['current_products_queryset']:
            for param in product.productparametervalue_set.all():
                if param.product_param_value_str:
                    context['product_param_str'].append(param.product_param_value_str)
                else:
                    context['product_param_int'].append({param.product_param.product_param_name: param.product_param_value_int})

                    #params_int_dict[param.product_param] = param.product_param_value_int
        end_time = time.time()
        elapsed_time = end_time - start_time
        print('Elapsed time2:', elapsed_time)
        """

        start_time = time.time()
        context['product_param_str'], context['product_param_int'] = {}, {}
        for product in context['current_products_queryset']:
            for param in product.productparametervalue_set.all():
                product_param = param.product_param
                value_int = param.product_param_value_int
                value_str = param.product_param_value_str
                param_by_filter = param.product_param_by_filter
                if product_param not in context['product_param_str'] and value_str and param_by_filter:
                    context['product_param_str'][product_param] = []
                if product_param not in context['product_param_int'] and value_int and param_by_filter:
                    context['product_param_int'][product_param] = [value_int, value_int]

                if value_str and param_by_filter and value_str.product_param_value_str not in \
                        context['product_param_str'][product_param]:
                    context['product_param_str'][product_param].append(value_str.product_param_value_str)
                if value_int and param_by_filter:
                    # value = param.product_param_value_int
                    # max_val = param.product_param_value_int
                    if context['product_param_int'][product_param][0] > value_int:
                        context['product_param_int'][product_param][0] = value_int
                    if context['product_param_int'][product_param][1] < value_int:
                        context['product_param_int'][product_param][1] = value_int

                    # context['product_param_int'][param_name] = (min_val, max_val)
                    # context['product_param_int'][param_name].append(param.product_param_value_int)
                    # min_val = min(context['product_param_int'][param_name])
                    # max_val = max(context['product_param_int'][param_name])

                    # params_int_dict[param.product_param] = param.product_param_value_int
        end_time = time.time()
        elapsed_time = end_time - start_time
        print('Elapsed time2:', elapsed_time)

        """
        start_time = time.time()
        context['product_param_str'] = [i for i in
                                        context['current_products_queryset'][0].productparametervalue_set.all()
                                        if i.product_param_value_str]
        context['product_param_int'] = [i for i in
                                        context['current_products_queryset'][0].productparametervalue_set.all()
                                        if i.product_param_value_int]

        end_time = time.time()
        elapsed_time = end_time - start_time
        print('Elapsed time3:', elapsed_time)
        """

        print(context['product_param_str'])
        print(context['product_param_int'])
        start_time = time.time()
        context['product_param_filter_str'] = [i.product_param_name for i in context['product_param_str']]
        context['product_param_filter_int'] = [i.product_param_name for i in context['product_param_int']]
        end_time = time.time()
        elapsed_time = end_time - start_time
        print('Elapsed time3:', elapsed_time)
        print(context['product_param_filter_str'])
        print(context['product_param_filter_int'])
        return context



"""
class ManufacturerViewSet(ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
"""


class ProductView(DetailView):
    template_name = 'store/product.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'

    def get_queryset(self):
        return (Product.objects.filter(
            slug=self.kwargs['product_slug'],
            subcategory__subcategory_slug=self.kwargs['subcategory_slug'],
            subcategory__category__category_slug=self.kwargs['category_slug'],
            subcategory__category__fishing_season__fishing_season_slug=self.kwargs['fishing_season_slug'])
                # .select_related('subcategory__category__fishing_season')
                .select_related('manufacturer')
                .prefetch_related(Prefetch('productparametervalue_set',
                                           queryset=ProductParameterValue.objects.all()
                                           .select_related('product_param', 'product_param_value_str')))
                # .prefetch_related('productparametervalue_set')
                # .prefetch_related('productparametervalue_set__product_param_value_str')
                # .prefetch_related('productparametervalue_set__product_param')
                .prefetch_related('additional_product_image')
                )

    # def get_object(self, queryset=None):
    #   return self.get_queryset().get(slug=self.kwargs['product_slug'])


"""
def product(request, fishing_season_slug, category_slug, subcategory_slug, slug):
    current_product = ProductParameterValue.objects.get(pk=product_id)
    basket_rod_form = BasketAddProductForm()
    context = {'current_rod': current_rod, 'basket_rod_form': basket_rod_form}
    return render(request, 'store/rod.html', context)
"""


def basket_add(request, rod_id):
    basket = Basket(request)
    product = get_object_or_404(Product, id=rod_id)
    basket.add(product=product)
    return redirect('basket_detail')


@require_POST
def basket_update_quantity(request, rod_id):
    basket = Basket(request)
    product = get_object_or_404(Product, id=rod_id)
    q_choices = [(i, str(i)) for i in range(1, 31)]  # максимальный стартовый выбор количества для всех товаров в козине
    form = BasketAddProductForm(request.POST)
    form.quantity_choices(q_choices)

    if form.is_valid():
        cd = form.cleaned_data
        basket.add(product=product,
                   quantity=cd['quantity'],
                   update_quantity=cd['update'])

    return redirect('basket_detail')


def basket_remove(request, product_id):
    """Функция представление для удаления товаров из корзины"""
    basket = Basket(request)
    product = get_object_or_404(Product, id=product_id)
    basket.remove(product)
    return redirect('basket_detail')


def basket_detail(request):
    """Функция представление для отображения корзины и ее товаров"""
    basket = Basket(request)
    for i in basket:
        bf = BasketAddProductForm(initial={'quantity': i['quantity'], 'update': True})
        bf.quantity_choices(i['quantity_choices'])
        i['update_quantity_form'] = bf

    return render(request, 'store/basket.html', {'basket': basket})


