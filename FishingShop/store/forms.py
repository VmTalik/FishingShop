from django import forms


class BasketAddProductForm(forms.Form):
    """Форма для обновления количества товаров в корзине"""
    def quantity_choices(self, choices):
        self.fields['quantity'] = forms.TypedChoiceField(choices=choices, coerce=int, label='')
        self.fields['update'] = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
