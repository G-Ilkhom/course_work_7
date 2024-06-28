import requests
from celery import shared_task
from django.conf import settings

from config.settings import TELEGRAM_BOT_API_KEY, TELEGRAM_CHAT_ID
from habits.models import Habit

BOT_TOKEN = TELEGRAM_BOT_API_KEY
telegram_id = TELEGRAM_CHAT_ID
get_id_url = f'{settings.TELEGRAM_URL}{BOT_TOKEN}/getUpdates'
send_message_url = f'{settings.TELEGRAM_URL}{BOT_TOKEN}/sendMessage'


@shared_task
def send_message_to_tg_bot(habit_id):
    """ Функция отправки сообщения в телеграм-бот """

    habit = Habit.objects.get(id=habit_id)
    print("Отправлено напоминание в телеграмм")
    requests.get(
        url=f'{settings.TELEGRAM_URL}{settings.TELEGRAM_BOT_API_KEY}/sendMessage',
        params={
            'chat_id': habit.owner.telegram_id,
            'text': f'Привет {habit.owner}!'
                    f'Время {habit.time} выполнить {habit.action}. Место - {habit.place}.'
                    f'Это займет {habit.time_required} минут!'
        }
    )
