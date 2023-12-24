from store.models import Manufacturer, FishingSeason, Product, ProductParameterValue, Category, SubCategory, Customer, \
    Step, BuyStep, BuyProduct, Buy, Comment
from store.serializers import ManufacturerSerializer, SubCategorySerializer, ProductSerializer
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views.decorators.http import require_POST
from .basket import Basket
from .forms import BasketAddProductForm, RegisterCustomerForm, BuyForm, \
    CustomerBuyForm, CustomerProfileDeliveryForm, CustomerProfileForm, CustomerCommentForm
import sys
from pympler.asizeof import asizeof
import time
from django.views.generic.detail import DetailView
from django.http import Http404
from django.views.generic import ListView, DetailView
from django.db.models import Prefetch
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
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


def product_categories(request, fishing_season_slug):
    # каталог категорий товаров в зависимости от рыболовного сезона
    product_categories_queryset = (
        (Category.objects.filter(fishing_season__fishing_season_slug=fishing_season_slug)
         .select_related('fishing_season')))
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
    context = {'product_subcategories_queryset': product_subcategories_queryset
               }
    if product_subcategories_queryset:
        return render(request, 'store/product_subcategories.html', context)
    else:
        raise Http404('Нет такой страницы с подкатегориями товаров!')


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
                .prefetch_related(Prefetch('comment_set',
                                           queryset=Comment.objects.all()
                                           .select_related('customer')))
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
        # задаем начальные минимльную и максимальную цену товара для фильтра
        context['min_price'] = context['current_products_queryset'][0].price
        context['max_price'] = context['current_products_queryset'][0].price
        context['products_evaluations'] = {}  # оценки товаров (среднее знач. оценок товара и количество оценок)
        for product in context['current_products_queryset']:
            product_comments = product.comment_set.all()  # Все отзывы к товару
            if product_comments:
                product_evaluations_sum = 0  # сумма оценок товара
                for product_comment in product_comments:
                    product_evaluations_sum += product_comment.evaluation
                evaluation_count = len(product_comments)  # количество оценок товара
                evaluation_average = round(product_evaluations_sum / evaluation_count, 2)  # средняя оценка товара
                context['products_evaluations'].update({product: (evaluation_average, evaluation_count)})

            # Опеределяем минимльную и максимальную цену товара для фильтра
            price = product.price
            if price < context['min_price']:
                context['min_price'] = price
            if price > context['max_price']:
                context['max_price'] = price
            # Опеределяем остальные параметры для фильтра - список названий чекбоксов, а также min и max параметров диапазона
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

    # form_class = CustomerCommentForm

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
                .prefetch_related(Prefetch('comment_set',
                                           queryset=Comment.objects.all()
                                           .select_related('customer')))
                )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['user_comment'] = Comment.objects.filter(customer=self.request.user)
        context['comment_form'] = CustomerCommentForm()
        evaluation_sum = 0  # сумма оценок товара
        comments = context['product'].comment_set.all()
        for comment in comments:
            evaluation_sum += comment.evaluation
            if comment.customer == self.request.user:
                context['user_comment'] = comment  # комментарий теущего пользователя
        if comments:
            context['evaluation_count'] = len(comments)
            context['product_evaluation_average'] = round(evaluation_sum / context['evaluation_count'], 2)
        return context

    def post(self, request, *args, **kwargs):
        form = CustomerCommentForm(request.POST)
        product = Product.objects.get(slug=self.kwargs['product_slug'])
        if form.is_valid():
            comment = form.save(commit=False)
            comment.title = 'title'
            comment.customer = self.request.user
            comment.product = product
            comment.save()

        self.object = self.get_object()
        return self.render_to_response(context=self.get_context_data())


"""
def product(request, fishing_season_slug, category_slug, subcategory_slug, slug):
    current_product = ProductParameterValue.objects.get(pk=product_id)
    basket_rod_form = BasketAddProductForm()
    context = {'current_rod': current_rod, 'basket_rod_form': basket_rod_form}
    return render(request, 'store/rod.html', context)
"""


def basket_add(request, product_id):
    basket = Basket(request)
    product = get_object_or_404(Product, id=product_id)
    basket.add(product=product)
    return redirect('basket_detail')


@require_POST
def basket_update_quantity(request, product_id):
    basket = Basket(request)
    product = get_object_or_404(Product, id=product_id)
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


def ordering(request):
    """Функция представление для формирования заказа клиентом"""
    user_id = request.user.pk
    customer_initial = Customer.objects.get(pk=user_id)
    if request.method == "POST":
        buy_form = BuyForm(request.POST)
        customer_form = CustomerBuyForm(request.POST, instance=customer_initial)
        if buy_form.is_valid() and customer_form.is_valid():
            basket = Basket(request)
            customer = customer_form.save(commit=False)
            customer.username = customer_initial.username
            customer.save()

            buy = buy_form.save(commit=False)
            buy.delivery_city = customer.city
            buy.delivery_region = customer.region
            buy.delivery_address = customer.delivery_address
            buy.buyer_full_name = f'{customer.last_name} {customer.first_name} {customer.patronymic}'
            buy.buyer_phone_number = customer.phone_number
            buy.customer_id = customer.pk  # эту строку попробовать заменить на buy.customer_id = customer
            buy.save()
            step = Step()
            if not Step.objects.get(step_name='Заказ создан'):
                step.step_name = 'Заказ создан'
                step.save()
            step = Step.objects.get(step_name='Заказ создан')

            BuyStep.objects.create(buy_id=buy.pk,
                                   step_id=step.pk)
            for item in basket:
                BuyProduct.objects.create(product_buy_id=buy.pk,
                                          product_id=item['product'].pk,
                                          product_amount=item['quantity'],
                                          product_price=item['price'])
            return redirect('successful_ordering')
    else:
        buy_form = BuyForm()
        customer_form = CustomerBuyForm(instance=customer_initial)

    return render(request,
                  'store/ordering.html',
                  {'buy_form': buy_form, 'customer_form': customer_form})


def successful_ordering(request):
    basket = Basket(request)
    basket.clear()
    return render(request, 'store/successful_ordering.html')


@login_required
def profile(request):
    """Функция представление - личный кабинет клиента"""
    customer = request.user
    products_buy = (Buy.objects.filter(customer=customer)
                    .prefetch_related('buyproduct_set')
                    .prefetch_related(Prefetch('buystep_set',
                                               queryset=BuyStep.objects.select_related('step')
                                               .order_by('-step_begin_date'))))
    orders = {}
    for buy in products_buy:
        products_count = 0
        products_price = 0
        for product in buy.buyproduct_set.all():
            products_count += product.product_amount
            products_price += product.product_price * product.product_amount
        orders[buy] = (products_count, products_price)

    profile_delivery_form = CustomerProfileDeliveryForm
    return render(request, 'store/profile.html',
                  {
                      'customer': customer,
                      'profile_delivery_form': profile_delivery_form,
                      'orders': orders
                  })


def order_tracking(request, buy_id):
    """Функция представление - трек ослеживания доставки в личном кабинете клиента"""
    products_bought = (BuyProduct.objects.filter(product_buy=buy_id)
                       .select_related('product__subcategory__category__fishing_season')
                       )
    buy_steps = BuyStep.objects.filter(buy=buy_id).order_by('-step_begin_date').select_related('step')
    total_products_price = 0
    for product in products_bought:
        total_products_price += product.product_price * product.product_amount

    return render(request, 'store/order_tracking.html',
                  {'products_bought': products_bought,
                   'buy_steps': buy_steps, 'buy_id': buy_id,
                   'total_products_price': total_products_price})


@login_required
def edit_delivery_address_profile(request):
    """Функция представление - редактирование адреса доставки в личном кабинете клиента"""
    customer = Customer.objects.get(pk=request.user.pk)
    if request.method == "POST":
        delivery_address_profile_form = CustomerProfileDeliveryForm(request.POST, instance=customer)
        if delivery_address_profile_form.is_valid():
            delivery_address_profile_form.save()
            return redirect('profile')
    else:
        delivery_address_profile_form = CustomerProfileDeliveryForm(instance=customer)
    return render(request, 'store/delivery_address_profile.html',
                  {'delivery_address_profile_form': delivery_address_profile_form})


@login_required
def edit_customer_profile(request):
    """Функция представление - редактирование личных данных в личном кабинете клиента"""
    customer = Customer.objects.get(pk=request.user.pk)
    if request.method == "POST":
        customer_profile_form = CustomerProfileForm(request.POST, instance=customer)
        if customer_profile_form.is_valid():
            customer_profile_form.save()
            return redirect('profile')
    else:
        customer_profile_form = CustomerProfileForm(instance=customer)
    return render(request, 'store/editing_customer_profile.html',
                  {'customer_profile_form': customer_profile_form})


class CustomerLoginView(LoginView):
    """Класс представление - вход клиента в личный кабинет """
    template_name = 'store/login.html'


class CustomerLogoutView(LoginRequiredMixin, LogoutView):
    """Класс представление - выход клиента из личного кабинета """
    template_name = 'store/logout.html'


class ChangeCustomerPasswordView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    """Класс представление - смена пароля клиента """
    template_name = 'store/password_change.html'
    success_url = reverse_lazy('profile')
    success_message = 'Изменение пароля прошло успешно!'


class RegisterCustomerView(CreateView):
    """Класс представление - регистрация клиента"""
    model = Customer
    template_name = 'store/register_customer.html'
    form_class = RegisterCustomerForm
    success_url = reverse_lazy('register_done')


class RegisterDoneView(TemplateView):
    """Класс представление - вывод сообщения об успешной регистрации"""
    template_name = 'store/register_done.html'


def customer_activate(request, sign):
    """Функция представление - активация нового пользователя (клиента)"""
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'store/bad_signature.html')
    user = get_object_or_404(Customer, username=username)
    if user.is_activated:
        template = 'store/customer_is_activated.html'
    else:
        template = 'store/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


class DeleteCustomerAccountView(LoginRequiredMixin, DeleteView):
    """Класс представление - удаление аккаунта клиента"""
    model = Customer
    template_name = 'store/delete_customer.html'
    success_url = reverse_lazy('index')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь успешно удален')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class ResetCustomerPasswordView(PasswordResetView):
    """Класс представление - инициализация процедуры сброса пароля. Отправка клиенту письма для сброса пароля"""
    # form_class = PasswordResetForm
    template_name = 'email/reset_password.html'
    subject_template_name = 'email/reset_subject.txt'
    email_template_name = 'email/reset_email.txt'
    success_url = reverse_lazy('password_reset_notification')


class ResetDoneCustomerPasswordView(PasswordResetDoneView):
    """Класс представление - вывод уведомления об успешной отправке письма о сбросе пароля """
    template_name = 'email/email_sent.html'


class ResetConfirmCustomerPasswordView(PasswordResetConfirmView):
    """Класс представление -сброс пароля клиента"""
    # form_class = SetPasswordForm
    template_name = 'email/password_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class ResetCompleteCustomerPasswordView(PasswordResetCompleteView):
    """Класс представление - уведомление об успешном сбросе пароля"""
    template_name = 'email/password_confirmed.html'
