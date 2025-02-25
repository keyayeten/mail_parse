from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from encrypted_model_fields.fields import EncryptedCharField


class CustomUser(AbstractUser):
    email_password = EncryptedCharField(max_length=100, blank=True)

    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set', blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
