from django.conf import settings
from decimal import Decimal
from .models import Product


class Basket:
    def __init__(self, request):
        """Метод инициализации корзины"""
        # текущая сессия
        self.session = request.session
        # попытка получить корзину с текущей сессии
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if not basket:
            # если в сессии нет корзины, то создаем пустую корзину
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket

    def add(self, product, quantity=1, update_quantity=False):
        """Метод добавления товара в корзину или же обновления его количества"""
        product_id = str(product.id)
        if product_id not in self.basket:
            self.basket[product_id] = {'quantity': 0,
                                       'quantity_choices': [(i, str(i)) for i in range(1, product.quantity + 1)],
                                       'price': str(product.price)
                                       }
        if update_quantity:
            self.basket[product_id]['quantity'] = quantity
        else:
            self.basket[product_id]['quantity'] += quantity
        self.save()

    def check_product(self):
        """Метод проверки наличия товара на складе. Если товара на складе меньше чем было заказано,
        то уведомить покупателя и запретить покупку, можно купить только столько сколько на складе есть
        """
        pass

    def save(self):
        """Метод сохранения изменений корзины в сессии"""
        # Обновление сессии basket
        self.session[settings.BASKET_SESSION_ID] = self.basket
        # Пометка сеанса как "измененный", чтобы убедиться, что сеанс сохранен
        self.session.modified = True

    def remove(self, product):
        """Метод удаления товара из корзины"""
        product_id = str(product.id)
        if product_id in self.basket:
            del self.basket[product_id]
        self.save()

    def __iter__(self):
        """Метод перебора элементов в корзине и получение продуктов из базы данных"""
        product_ids = self.basket.keys()
        # получение объектов product и добавление их в корзину
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.basket[str(product.id)]['product'] = product

        for item in self.basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """ Метод определения количества всех товаров в корзине"""
        return sum(item['quantity'] for item in self.basket.values())

    def get_total_price(self):
        """Метод определения общей стоимости для каждого товара в корзине"""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.basket.values())

    def clear(self):
        """Метод удаления сеанса корзины из сессии"""
        del self.session[settings.BASKET_SESSION_ID]
        self.session.modified = True
