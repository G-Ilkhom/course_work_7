from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from habits.models import Habit
from habits.paginations import HabitPaginator
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer
from habits.service import create_schedule


class HabitListAPIView(generics.ListAPIView):
    """ Вывод привычек пользователя """

    queryset = Habit.objects.all()
    serializer_class = Habit
