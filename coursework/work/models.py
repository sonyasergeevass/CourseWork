from django.db import models


class Customer(models.Model):
    """Customer model"""

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
