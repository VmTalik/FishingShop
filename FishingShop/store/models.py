from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class Manufacturer(models.Model):
    manufacturer_name = models.CharField(max_length=35, unique=True, verbose_name='Название производителя')
    brand_country = models.CharField(max_length=35, verbose_name="Страна производителя")

    def __str__(self):
        return self.manufacturer_name

    class Meta:
        verbose_name_plural = 'Производители'
        verbose_name = 'Производитель'


class Customer(AbstractUser):
    patronymic = models.CharField(max_length=30, verbose_name='Отчество', null=True, blank=True)
    send_messages = models.BooleanField(default=True, verbose_name='Высылать оповещения о новых товарах?')
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name="Прошел активацию?")
    phone_number = models.CharField(max_length=17, unique=True, verbose_name='Номер телефона', null=True, blank=True)
    city = models.CharField(max_length=25, verbose_name='Город', null=True, blank=True)
    region = models.CharField(max_length=25, verbose_name='Область, край', null=True, blank=True)
    postcode = models.SmallIntegerField(verbose_name='Почтовый индекс', null=True, blank=True)
    delivery_address = models.CharField(max_length=150, verbose_name='Адрес доставки', null=True, blank=True)

    class Meta(AbstractUser.Meta):
        verbose_name_plural = 'Клиенты'
        verbose_name = 'Клиент'


class FishingSeason(models.Model):
    fishing_season_name = models.CharField(max_length=20, unique=True, verbose_name='Название сезона рыбалки')
    fishing_season_slug = models.SlugField(max_length=20, unique=True, verbose_name='Слаг для сезона рыбалки')

    def __str__(self):
        return self.fishing_season_name

    class Meta:
        verbose_name_plural = 'Сезоны рыбалки'
        verbose_name = 'Сезон рыбалки'

    def get_absolute_url(self):
        return reverse('product_categories',
                       kwargs={'fishing_season_slug': self.fishing_season_slug})


class Category(models.Model):
    category_name = models.CharField(max_length=45, unique=True, verbose_name='Название категории товаров')
    category_slug = models.SlugField(max_length=30, unique=True, verbose_name='Слаг для категории товара')
    category_image = models.ImageField(upload_to='product_categories_images/',
                                       verbose_name='Изображение категории товаров')
    fishing_season = models.ForeignKey(FishingSeason, on_delete=models.CASCADE, verbose_name='Сезон рыбалки')

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = 'Категории товаров'
        verbose_name = 'Категория товара'

    def get_absolute_url(self):
        return reverse('product_subcategories',
                       kwargs={'fishing_season_slug': self.fishing_season.fishing_season_slug,
                               'category_slug': self.category_slug})


class SubCategory(models.Model):
    subcategory_name = models.CharField(max_length=45, unique=True, verbose_name='Название подкатегории товаров')
    subcategory_slug = models.CharField(max_length=30, verbose_name='Слаг для подкатегории товара')
    subcategory_image = models.ImageField(upload_to='product_subcategories_images/',
                                          verbose_name='Изображение подкатегории товаров')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория товаров')

    def __str__(self):
        return self.subcategory_name

    class Meta:
        verbose_name_plural = 'Подкатегории товаров'
        verbose_name = 'Подкатегория товара'

    def get_absolute_url(self):
        return reverse('products',
                       kwargs={
                           'fishing_season_slug': self.category.fishing_season.fishing_season_slug,
                           'category_slug': self.category.category_slug,
                           'subcategory_slug': self.subcategory_slug})


class Warehouse(models.Model):
    product_availability = models.CharField(max_length=30, unique=True, verbose_name='Наличие товара на складе')

    def __str__(self):
        return self.product_availability

    class Meta:
        verbose_name_plural = 'Наличие товаров на складе'
        verbose_name = 'Наличие товара на складе'


class AdditionalProductImage(models.Model):
    add_product_image = models.ImageField(upload_to='additional_product_images/',
                                          verbose_name='Дополнительное фото товара')

    class Meta:
        verbose_name_plural = 'Дополнительные фото товара'
        verbose_name = 'Дополнительное фото товара'


class Product(models.Model):
    name = models.CharField(max_length=60, unique=True, verbose_name='Название товара')
    slug = models.SlugField(max_length=30, unique=True, verbose_name='Артикул товара')
    price = models.PositiveIntegerField(verbose_name='Цена товара в руб.')
    description = models.TextField(verbose_name='Описание товара')
    image = models.ImageField(upload_to='product_images/', verbose_name='Основное фото товара')
    supply_date = models.DateField(verbose_name='Дата поступления товара', null=True)
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество единиц товара', null=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, verbose_name='Подкатегория товара')
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name='Производитель товара')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True,
                                  verbose_name='Наличие товара на складе')
    additional_product_image = models.ManyToManyField(AdditionalProductImage, verbose_name='Дополнительные фото товара')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Товары'
        verbose_name = 'Товар'

    def get_absolute_url(self):
        return reverse('product',
                       kwargs={
                           'fishing_season_slug': self.subcategory.category.fishing_season.fishing_season_slug,
                           'category_slug': self.subcategory.category.category_slug,
                           'subcategory_slug': self.subcategory.subcategory_slug,
                           'product_slug': self.slug})


class ProductParameter(models.Model):
    product_param_name = models.CharField(max_length=35, unique=True, verbose_name='Название параметра товара')
    product_param_slug = models.SlugField(max_length=25, unique=True, verbose_name='Слаг для названия параметра товара')

    def __str__(self):
        return self.product_param_name

    class Meta:
        verbose_name_plural = 'Названия параметров товара'
        verbose_name = 'Название параметра товара'


class ProductParameterValueStr(models.Model):
    product_param_value_str = models.CharField(max_length=35, unique=True,
                                               verbose_name='Строковое значение параметра товара')

    def __str__(self):
        return self.product_param_value_str

    class Meta:
        verbose_name_plural = 'Строковые значения параметров товара'
        verbose_name = 'Строковое значение параметра товара'


class ProductParameterValue(models.Model):
    MEASURE_UNIT_CHOICES = [
        ('м', 'м'), ('см', 'см'), ('мм', 'мм'), ('кг', 'кг'), ('гр', 'гр'), ('шт', 'шт')
    ]
    product_param_value_int = models.PositiveSmallIntegerField(verbose_name='Целое значение параметра товара',
                                                               null=True, blank=True)
    product_param_measure_unit = models.CharField(max_length=2, choices=MEASURE_UNIT_CHOICES,
                                                  verbose_name='Единица измерения параметра товара',
                                                  null=True, blank=True)
    product_param_by_filter = models.BooleanField(default=True, verbose_name='Указать параметр товара в фильтре')
    product_param_value_str = models.ForeignKey(ProductParameterValueStr, on_delete=models.SET_NULL,
                                                verbose_name='Строковое значение параметра товара',
                                                null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    product_param = models.ForeignKey(ProductParameter, on_delete=models.SET_NULL,
                                      verbose_name='Название параметра товара', null=True, blank=True)

    def __str__(self):
        return f'{self.product_param}-->{self.product}'

    class Meta:
        verbose_name_plural = 'Дополнительные параметры удилищ'
        verbose_name = 'Дополнительный параметр удилища'
        constraints = [models.UniqueConstraint(fields=['product_param', 'product'],
                                               name='unique_product_param_product')]
        # ограничение уникальности на два поля


class Buy(models.Model):
    wishes = models.TextField(verbose_name='Пожелания к заказу', null=True, blank=True)
    delivery_date = models.DateField(verbose_name='Желаемая дата доставки', null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Заказы'
        verbose_name = 'Заказ'


class Step(models.Model):
    step_name = models.CharField(max_length=30, unique=True, verbose_name='Название стадии покупки')

    def __str__(self):
        return self.step_name

    class Meta:
        verbose_name_plural = 'Названия стадий покупок'
        verbose_name = 'Название стадии покупки'


class BuyStep(models.Model):
    step_begin_date = models.DateField(verbose_name='Дата начала стадии покупки', auto_now_add=True)
    step_end_date = models.DateField(verbose_name='Дата конца стадии покупки', null=True, blank=True)
    buy = models.ForeignKey(Buy, on_delete=models.CASCADE)
    step = models.ForeignKey(Step, on_delete=models.CASCADE)


class BuyProduct(models.Model):
    product_amount = models.PositiveSmallIntegerField(verbose_name='Количество покупаемых товаров')
    product_price = models.PositiveIntegerField(verbose_name='Цена товара в руб.')
    product_buy = models.ForeignKey(Buy, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)


class Comment(models.Model):
    EVALUATION_CHOICES = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    title = models.CharField(max_length=60, verbose_name='Заголовок комментария')
    evaluation = models.PositiveSmallIntegerField(verbose_name='Оценка', choices=EVALUATION_CHOICES, default=5)
    comment_text = models.CharField(max_length=180, verbose_name='Текст комментария')
    comment_date = models.DateField(verbose_name='Дата комментария', auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True) #null убрать!

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Отзывы клиентов'
        verbose_name = 'Отзыв клиента'
