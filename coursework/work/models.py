from django.db import models


class Customers(models.Model):
    """Customers model"""

    class Meta:
        db_table = 'customers'
        managed = False
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"

    customer_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(verbose_name="Имя", max_length=50,
                                     null=True, blank=True)
    customer_lastname = models.CharField(verbose_name="Фамилия", max_length=50,
                                         null=True, blank=True)
    customer_surename = models.CharField(verbose_name="Отчество",
                                         max_length=50, null=True, blank=True)
    customer_email = models.EmailField(verbose_name="Почта", max_length=100,
                                       unique=True)
    customer_phone = models.CharField(verbose_name="Телефон", max_length=15,
                                      null=True, blank=True)
    customer_datebirth = models.DateField(verbose_name="Дата рождения",
                                          null=True, blank=True)
    customer_password = models.CharField(verbose_name="Пароль", max_length=100,
                                         unique=True)
    customer_photo = models.TextField(verbose_name="Фотография", null=True,
                                      blank=True)

    def __str__(self):
        return f"{self.customer_lastname} {self.customer_name}"


class Addresses(models.Model):
    """Addresses model"""

    class Meta:
        db_table = 'addresses'
        managed = False
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"

    address_id = models.AutoField(primary_key=True)
    ad_customer = models.ForeignKey('Customers', on_delete=models.RESTRICT,
                                    db_column='ad_customer',
                                    verbose_name='ФИО покупателя')
    ad_country = models.CharField(verbose_name="Страна", max_length=100)
    ad_region = models.CharField(verbose_name="Регион/край", max_length=100)
    ad_city = models.CharField(verbose_name="Город", max_length=100)
    ad_street = models.CharField(verbose_name="Улица", max_length=100)
    ad_house = models.IntegerField(verbose_name="Дом")
    ad_building = models.IntegerField(verbose_name="Строение", null=True,
                                      blank=True)
    ad_apartment = models.IntegerField(verbose_name="Квартира", null=True,
                                       blank=True)
    ad_index = models.IntegerField(verbose_name="Индекс")


class Status(models.Model):
    """Status model"""

    class Meta:
        db_table = "status"
        managed = False
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(verbose_name="Статус заказа", max_length=20,
                                   unique=True)

    def __str__(self):
        return f"{self.status_name}"


class Categories(models.Model):
    """Categories model"""

    class Meta:
        db_table = 'categories'
        managed = False
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(verbose_name="Категория товара",
                                     max_length=70, unique=True)

    def __str__(self):
        return f"{self.category_name}"


class Products(models.Model):
    """Products model"""

    class Meta:
        db_table = "products"
        managed = False
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    product_id = models.AutoField(primary_key=True)
    prod_name = models.CharField(verbose_name="Название товара",
                                 max_length=100, unique=True)
    prod_description = models.TextField(verbose_name="Описание товара",
                                        null=True, blank=True)
    prod_photo = models.TextField(verbose_name="Ссылка на фото товара",
                                  null=True, blank=True)
    prod_amount = models.IntegerField(verbose_name="Количество товара",
                                      null=True, blank=True, default=0)
    prod_category = models.ForeignKey('Categories', on_delete=models.RESTRICT,
                                      db_column='prod_category',
                                      verbose_name='Категория товара')
    prod_sell_price = models.DecimalField(verbose_name="Цена продажи",
                                          max_digits=10, decimal_places=2,
                                          default=0.00)
    prod_supply_price = models.DecimalField(verbose_name="Цена поставки",
                                            max_digits=10, decimal_places=2,
                                            default=0.00)

    def __str__(self):
        return f"{self.prod_name}"

    def description(self):
        return self.prod_description[:40] + "..." \
            if self.prod_description else 'Описание отсутсвует'

    description.short_description = 'Описание товара'

    def link_on_photo(self):
        return self.prod_photo[:40] + "..." \
            if self.prod_photo else 'Ссылка отсутсвует'

    link_on_photo.short_description = 'Ссылка на изображение'


class Supplies(models.Model):
    """Supplies model"""

    class Meta:
        db_table = 'supplies'
        managed = False
        verbose_name = "Поставка"
        verbose_name_plural = "Поставки"

    supply_id = models.AutoField(primary_key=True)
    sup_product = models.ForeignKey('Products', on_delete=models.RESTRICT,
                                    db_column='sup_product',
                                    verbose_name='Название товара')
    sup_amount = models.IntegerField(verbose_name='Количество товара')


class Orders(models.Model):
    """Orders model"""

    class Meta:
        db_table = 'orders'
        managed = False
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    order_id = models.AutoField(primary_key=True)
    order_date = models.DateTimeField(verbose_name='Дата заказа',
                                      auto_now_add=True)
    ord_customer = models.ForeignKey('Customers', on_delete=models.RESTRICT,
                                     db_column='ord_customer',
                                     verbose_name='Покупатель')
    ord_status = models.ForeignKey('Status', on_delete=models.RESTRICT,
                                   db_column='ord_status',
                                   verbose_name='Статус')

    def __str__(self):
        return f"{self.order_id}"


class OrderItems(models.Model):
    """OrderItems model"""

    class Meta:
        db_table = 'order_items'
        managed = False
        verbose_name = "Состав заказа"
        verbose_name_plural = "Состав заказов"
        unique_together = ('oi_order', 'oi_product')

    oi_id = models.AutoField(primary_key=True)
    oi_order = models.ForeignKey('Orders', on_delete=models.RESTRICT,
                                 db_column='oi_order',
                                 verbose_name='Номер заказа')
    oi_product = models.ForeignKey('Products', on_delete=models.RESTRICT,
                                   db_column='oi_product',
                                   verbose_name='Название товара')
    oi_amount = models.IntegerField(default=1,
                                    verbose_name='Количество единиц товара')
