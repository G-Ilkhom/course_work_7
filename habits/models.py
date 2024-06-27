from datetime import timedelta
from django.db import models
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Habit(models.Model):
    """ Модель привычки """

    DAILY = 'ежедневно'
    WEEKLY = 'еженедельно'

    PERIODICITY_SELECTION = ((DAILY, 'ежедневно'), (WEEKLY, 'еженедельно'))
    owner = models.ForeignKey(User, verbose_name='Владелец', related_name='habits', on_delete=models.CASCADE,
                              **NULLABLE)
    name = models.CharField(max_length=100, verbose_name='Название привычки')
    place = models.CharField(max_length=100, verbose_name='Место выполнения привычки', **NULLABLE)
    time = models.TimeField(verbose_name='Время выполнения привычки', **NULLABLE)
    action = models.CharField(max_length=100, verbose_name='Действие привычки')
    pleasant_habit = models.BooleanField(default=True, verbose_name='Признак приятной привычки')
    linked_habit = models.ForeignKey('self', verbose_name='Связанная привычка', on_delete=models.CASCADE, **NULLABLE)
    periodicity = models.CharField(max_length=20, verbose_name='Периодичность привычки', choices=PERIODICITY_SELECTION,
                                   default=DAILY)
    reward = models.CharField(max_length=100, verbose_name='Вознаграждение', **NULLABLE)
    time_required = models.DurationField(default=timedelta(minutes=2), verbose_name='Время на выполнение привычки')
    public_visibility = models.BooleanField(default=True, verbose_name='Признак публичной привычки')

    def __str__(self):
        return f'{self.owner} будет делать {self.action} в {self.time} в {self.place}'

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
