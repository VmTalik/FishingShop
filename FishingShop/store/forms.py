from django import forms

from .apps import user_registered
from .models import Customer, Buy, Comment

from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError


class BasketAddProductForm(forms.Form):
    """Форма для обновления количества товаров в корзине"""
    def quantity_choices(self, choices):
        self.fields['quantity'] = forms.TypedChoiceField(choices=choices, coerce=int, label='')
        self.fields['update'] = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class CustomerBuyForm(forms.ModelForm):
    """Форма данных клиента при оформлении заказа"""

    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'patronymic', 'email', 'city', 'region',
                  'phone_number', 'postcode', 'delivery_address')


class CustomerProfileDeliveryForm(forms.ModelForm):
    """Форма данных клиента в профиле для доставки """

    class Meta:
        model = Customer
        fields = ('city', 'region', 'postcode', 'delivery_address')


class CustomerProfileForm(forms.ModelForm):
    """Форма личных данных клиента в профиле"""
    email = forms.EmailField(required=True, label='Электронная почта')

    class Meta:
        model = Customer
        fields = ('username', 'email', 'first_name', 'last_name', 'patronymic', 'phone_number', 'send_messages')


class BuyForm(forms.ModelForm):
    """Форма с допольнительными данными при оформлении заказа"""

    class Meta:
        model = Buy
        fields = ('wishes',)


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
