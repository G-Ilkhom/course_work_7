from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    """ Модель пользователя """

    STATUS_SELECTION = ((True, 'Действующий'), (False, 'Заблокирован'))

    username = None
    email = models.EmailField(unique=True, verbose_name='Почта', help_text='Укажите почту')
    phone = models.CharField(max_length=35, verbose_name='Телефон', help_text='Укажите телефон', **NULLABLE)
    city = models.CharField(max_length=100, verbose_name='Город', help_text='Укажите город', **NULLABLE)
    avatar = models.ImageField(upload_to='users/avatars', verbose_name='Аватар', help_text='Укажите аватар', **NULLABLE)
    is_active = models.BooleanField(choices=STATUS_SELECTION, default=True, verbose_name='Статус пользователя')
    telegram_id = models.CharField(max_length=20, verbose_name='Id телеграмма', help_text='Укажите id телеграмма',
                                   **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
