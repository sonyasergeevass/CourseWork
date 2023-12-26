import re

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
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


@receiver(post_save, sender=User)
def convert_photo_link_to_direct_link(sender, instance, created, **kwargs):
    try:
        if instance.photo:
            match = re.search(r'/d/([^/]+)/view', instance.photo)
            if match:
                file_id = match.group(1)
                instance.photo = ('https://drive.google.com/uc?id=' + file_id)
                instance.save()
    except Exception as e:
        print(f"Произошла ошибка: {e}")
