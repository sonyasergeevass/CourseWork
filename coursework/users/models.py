from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(
        _('email address'),
        unique=True,
    )

    sure_name = models.CharField(_("Отчество"),
                                 max_length=50, null=True, blank=True)
    phone = models.CharField(_('Номер телефона'), max_length=15,
                             null=True,
                             blank=True)
    datebirth = models.DateField(_('Дата рождения'), null=True, blank=True)
    photo = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
