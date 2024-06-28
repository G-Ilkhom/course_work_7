from datetime import timedelta

from rest_framework.serializers import ValidationError

days = timedelta(days=7)
time = timedelta(minutes=2)


def validator_for_habit(value):
    """Валидация привычки"""

    try:
        if value["pleasant_habit"]:
            if value["linked_habit"] or value["reward"]:
                raise ValidationError(
                    "У приятной привычки не может быть вознаграждения или связанной привычки."
                )
    except KeyError:
        pass

    try:
        if value["linked_habit"] and value["reward"]:
            raise ValidationError(
                "Можно выбрать или связанную привычку или вознаграждение"
            )
    except KeyError:
        pass

    try:
        if value["linked_habit"]:
            if not value["linked_habit"].pleasant_habit:
                raise ValidationError(
                    "В связанные привычки могут попадать только привычки с признаком приятной привычки"
                )
    except KeyError:
        pass

    try:
        if not 0 < value["periodicity"] <= days:
            raise ValidationError(
                "Привычку можно выполнять не реже, чем 1 раз в 7 дней"
            )
    except KeyError:
        pass

    try:
        if value["time_required"] > time:
            raise ValidationError("Привычку можно выполнять не более 120 секунд")
    except KeyError:
        pass
