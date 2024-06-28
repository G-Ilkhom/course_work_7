import pytz
from config import settings
from datetime import datetime
from django_celery_beat.models import CrontabSchedule
from django_celery_beat.models import PeriodicTask
from django.http import HttpResponse
from habits.models import Habit
from habits.tasks import send_message_to_tg_bot, telegram_id


def check_daily_habits():
    """ Проверка ежедневных привычек на выполнение """

    datetime_now = datetime.now()
    moscow_timezone = pytz.timezone('Europe/Moscow')
    date_now = datetime_now.astimezone(moscow_timezone)
    time_now = date_now.time()
    habits = Habit.objects.filter(time__hour=time_now.hour, time__minute=time_now.minute,
                                  periodicity='ежедневно', pleasant_habit=False)

    for habit in habits:
        create_message(habit.id)


def check_weekly_habits():
    """ Проверка еженедельных привычек на выполнение """

    datetime_now = datetime.now()
    moscow_timezone = pytz.timezone('Europe/Moscow')
    date_now = datetime_now.astimezone(moscow_timezone)
    time_now = date_now.time()
    habits = Habit.objects.filter(time__hour=time_now.hour, time__minute=time_now.minute,
                                  periodicity='еженедельно', pleasant_habit=False)

    for habit in habits:
        create_message(habit.id)


def create_message(habit_id):
    """ Функция создания сообщения для отправки в телеграм-бот """

    habit = Habit.objects.get(id=habit_id)
    owner = habit.owner
    time = habit.time
    place = habit.place
    action = habit.action
    time_required = round(habit.time_required.total_seconds() / 60)

    message = f'Привет {owner}! Время {time}. Пора идти в {place} и сделать {action}. ' \
              f'Это займет {time_required} минут!'

    response = send_message_to_tg_bot(telegram_id, message)
    if habit.linked_habit:
        pleasant_habit_id = habit.linked_habit.id
        pleasant_habit = Habit.objects.get(id=pleasant_habit_id)
        nice_time = round(pleasant_habit.time_required.total_seconds() / 60)
        message = (f'Молодец! Ты выполнил {action}, за это тебе подарок {pleasant_habit.action} '
                   f'в течение {nice_time} минут')
        time.sleep(10)
        nice_response = send_message_to_tg_bot(telegram_id, message)
        return HttpResponse(nice_response)

    return HttpResponse(response)


def create_schedule(habit):
    """ Создание задачи """

    crontab_schedule, _ = CrontabSchedule.objects.get_or_create(
        minute=habit.time.minute,
        hour=habit.time.hour,
        day_of_week='*' if habit.periodicity == 'ежедневно' else '*/7',
        month_of_year='*',
        timezone=settings.TIME_ZONE
    )

    PeriodicTask.objects.create(
        crontab=crontab_schedule,
        name=f'Привычка - {habit.action}',
        task='habits.tasks.send_message_to_tg_bot',
        args=[habit.id],
    )


def delete_schedule(habit):
    """ Удаление задачи """

    task_name = f'send_message_to_tg_bot{habit.id}'
    PeriodicTask.objects.filter(name=task_name).delete()


def update_schedule(habit):
    """ Обновление задачи """

    delete_schedule(habit)
    create_schedule(habit)
