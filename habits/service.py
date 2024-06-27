from config import settings
from django_celery_beat.models import CrontabSchedule, PeriodicTask


def create_schedule(habit):
    """ Создание задачи """

    crontab_schedule, _ = CrontabSchedule.objects.get_or_create(
        minute=habit.time.minute,
        hour=habit.time.hour,
        day_of_week='*' if habit.period == 'ежедневно' else '*/7',
        month_of_year='*',
        timezone=settings.TIME_ZONE
    )

    PeriodicTask.objects.create(
        crontab=crontab_schedule,
        name=f'Habit Task - {habit.name}',
        task='habits.tasks.send_message_to_bot',
        args=[habit.id],
    )