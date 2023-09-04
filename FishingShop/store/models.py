from django.db import models
from django.contrib.auth.models import AbstractUser


class Manufacturer(models.Model):
    manufacturer_name = models.CharField(max_length=45, unique=True, verbose_name='Название производителя')
    brand_country = models.CharField(max_length=35, verbose_name="Страна производителя")

    def __str__(self):
        return self.manufacturer_name


class Customer(AbstractUser):
    send_messages = models.BooleanField(default=True, verbose_name='Высылать оповещения о новых товарах?')

    class Meta(AbstractUser.Meta):
        pass


class RodType(models.Model):
    rod_type_name = models.CharField(max_length=35, unique=True, verbose_name='Тип удилища')
    rod_type_image = models.ImageField(upload_to='images_rod_type/', verbose_name='Фото удилища')

    class Meta:
        verbose_name_plural = 'Типы удилищ'
        verbose_name = 'Тип удилища'


class Rod(models.Model):
    rod_name = models.CharField(max_length=60, unique=True, verbose_name='Название удилища')
    rod_item_number = models.CharField(max_length=35, unique=True, verbose_name='Артикул удилища')
    rod_length = models.CharField(max_length=35, unique=True, verbose_name='Длина удилища')
    rod_handle_length = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Длина рукояти удилища')
    rod_weight = models.DecimalField(max_digits=6, decimal_places=3, verbose_name='Масса удилища')
    rod_rings_number = models.SmallIntegerField(verbose_name='Количество колец удилища')
    rod_description = models.TextField(verbose_name='Описание удилища')
    rod_price = models.IntegerField(verbose_name='Цена удилища в руб.')
    rod_image = models.ImageField(upload_to='images_rods/', verbose_name='Основное фото удилища')
    rod_image_add1 = models.ImageField(upload_to='additional_images_rods/', verbose_name='Дополнительное фото удилища',
                                       blank=True)
    rod_image_add2 = models.ImageField(upload_to='additional_images_rods/', verbose_name='Дополнительное фото удилища',
                                       blank=True)
    rod_type_id = models.ForeignKey(RodType, on_delete=models.CASCADE, verbose_name='Тип удилища')
    rod_manufacturer_id = models.ForeignKey(Manufacturer, on_delete=models.CASCADE,
                                            verbose_name='Производитель удилища')

    class Meta:
        verbose_name_plural = 'Удилища'
        verbose_name = 'Удилище'


class ReelType(models.Model):
    reel_type_name = models.CharField(max_length=35, unique=True, verbose_name='Тип катушки')
    reel_type_image = models.ImageField(verbose_name='Фото катушки')


class Reel(models.Model):
    reel_name = models.CharField(max_length=60, unique=True, verbose_name='Название катушки')
    reel_item_number = models.CharField(max_length=35, unique=True, verbose_name='Артикул катушки')
    number_reel_bearings = models.SmallIntegerField(verbose_name='Количество подшипников катушки')
    reel_gear_ratio = models.SmallIntegerField(verbose_name='Передаточное отношение катушки')
    reel_capaсity = models.CharField(max_length=20, unique=True, verbose_name='Лесоемкость катушки')
    reel_spool_size = models.SmallIntegerField(verbose_name='Размер шпули катушки')
    reel_weight = models.DecimalField(max_digits=6, decimal_places=3, verbose_name='Масса катушки')
    reel_friction_type = models.CharField(max_length=45, unique=True,
                                          verbose_name='Тип фрикциона')  # сделать поле выбора
    reel_description = models.TextField(verbose_name='Описание катушки')
    reel_price = models.IntegerField(verbose_name='Цена катушки')
    reel_image = models.ImageField(verbose_name='Фото катушки')
    reel_type_id = models.ForeignKey(ReelType, on_delete=models.CASCADE)
    reel_manufacturer_id = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)


class Buy(models.Model):
    buy_description = models.TextField(verbose_name='Пожелания к заказу')
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Step(models.Model):
    step_name = models.CharField(max_length=30, unique=True,
                                 verbose_name='Название стадии покупки')  # сделать поле выбора


class BuyStep(models.Model):
    step_begin_date = models.DateField(verbose_name='Дата начала стадии покупки')
    step_end_date = models.DateField(verbose_name='Дата конца стадии покупки')
    buy_id = models.ForeignKey(Buy, on_delete=models.CASCADE)
    step_id = models.ForeignKey(Step, on_delete=models.CASCADE)


class BuyRod(models.Model):
    rod_amount = models.SmallIntegerField(verbose_name='Количество покупаемых удочек')
    rod_buy_id = models.ForeignKey(Buy, on_delete=models.CASCADE)
    rod_id = models.ForeignKey(Rod, on_delete=models.CASCADE)


class BuyReel(models.Model):
    reel_amount = models.SmallIntegerField(verbose_name='Количество покупаемых катушек')
    reel_buy_id = models.ForeignKey(Buy, on_delete=models.CASCADE)
    reel_id = models.ForeignKey(Reel, on_delete=models.CASCADE)


class Comment(models.Model):
    title = models.CharField(max_length=60, unique=True, verbose_name='Заголовок комментария')
    evaluation = models.SmallIntegerField(verbose_name='Оценка')  # сделать поле выбора
    comment_text = models.CharField(max_length=30, unique=True, verbose_name='Текст комментария')
    comment_date = models.DateField(verbose_name='Дата комментария')
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    rod_id = models.ForeignKey(Rod, on_delete=models.CASCADE)
    reel_id = models.ForeignKey(Reel, on_delete=models.CASCADE)
