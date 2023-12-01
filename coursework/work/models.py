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
    customer_email = models.EmailField(verbose_name="Почта", unique=True,
                                       null=True, blank=True)
    customer_phone = models.CharField(verbose_name="Телефон", max_length=15,
                                      null=True, blank=True)
    customer_datebirth = models.DateField(verbose_name="Дата рождения",
                                          null=True, blank=True)
    customer_login = models.CharField(verbose_name="Логин", max_length=100,
                                      unique=True)
    customer_password = models.CharField(verbose_name="Пароль", max_length=100,
                                         unique=True)
    customer_photo = models.TextField(verbose_name="Фотография", null=True,
                                      blank=True)


class Addresses(models.Model):
    """Addresses model"""

    class Meta:
        db_table = 'addresses'
        managed = False
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"

    address_id = models.AutoField(primary_key=True)
    ad_customer = models.ForeignKey('Customers', on_delete=models.RESTRICT,
                                    db_column='ad_customer')
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
    status_name = models.CharField(verbose_name="Статус заказа", max_length=20)


class Categories(models.Model):
    """Categories model"""

    class Meta:
        db_table = 'categories'
        managed = False
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=70)
