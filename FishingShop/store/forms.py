from django import forms

from .apps import user_registered
from .models import Customer, Buy, Comment

from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.forms.widgets import NumberInput
from django.core import validators


class BasketAddProductForm(forms.Form):
    """Форма для обновления количества товаров в корзине"""

    def quantity_choices(self, choices):
        self.fields['quantity'] = forms.TypedChoiceField(choices=choices, coerce=int, label='')
        self.fields['update'] = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class CustomerBuyForm(forms.ModelForm):
    """Форма данных клиента при оформлении заказа"""

    # делаем незаполненные поля формы только для чтения
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if self.instance.__dict__[field] is not None:
                self.fields[field].widget.attrs['readonly'] = True

    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'patronymic', 'email', 'city', 'region',
                  'phone_number', 'postcode', 'delivery_address')


class CustomerProfileDeliveryForm(forms.ModelForm):
    """Форма данных клиента в профиле для доставки """
    postcode = forms.CharField(validators=[validators.RegexValidator(regex=r'^\d{6}$')],
                               error_messages={'invalid': 'Ошибка ввода! Почтовый индекс должен состоять из 6-ти цифр'},
                               label='Почтовый индекс')

    class Meta:
        model = Customer
        fields = ('city', 'region', 'postcode', 'delivery_address')


class CustomerProfileForm(forms.ModelForm):
    """Форма личных данных клиента в профиле"""
    email = forms.EmailField(required=True, label='Электронная почта')
    phone_number = forms.CharField(
        validators=[validators.RegexValidator(regex=r'^(\+7|7|8)?(\s|-|\()?[(]?\d{3}[)]?[\s|-]?\d{3}-?\d{2}-?\d{2}$')],
        error_messages={'invalid': 'Неправильный формат номера телефона!'}, label='Номер телефона')

    class Meta:
        model = Customer
        fields = ('username', 'email', 'first_name', 'last_name', 'patronymic', 'phone_number', 'send_messages')


class BuyForm(forms.ModelForm):
    """Форма с дополнительными данными при оформлении заказа"""
    delivery_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}),
                                    label='Желаемая дата доставки',
                                    required=False)
    wishes = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}),
                             label='Пожелания к заказу',
                             required=False)

    class Meta:
        model = Buy
        fields = ('wishes', 'delivery_date')


class RegisterCustomerForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Электронная почта')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput,
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Повторно пароль', widget=forms.PasswordInput,
                                help_text='Введите пароль повторно')

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError('Ошибка. Введеные пароли разные!', code='password_mismatch')}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_registered.send(RegisterCustomerForm, instance=user)
        return user

    class Meta:
        model = Customer
        fields = ('username', 'email', 'password1', 'password2', 'first_name',
                  'last_name', 'send_messages')


class CustomerCommentForm(forms.ModelForm):
    comment_text = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label='Текст комментария')

    class Meta:
        model = Comment
        exclude = ('title', 'customer', 'product', 'comment_date')
