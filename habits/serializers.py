from rest_framework import serializers

from habits.models import Habit
from habits.validators import validator_for_habit


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Habit"""

    class Meta:
        model = Habit
        fields = "__all__"

        validators = [
            validator_for_habit,
        ]
