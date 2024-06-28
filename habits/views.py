from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from habits.models import Habit
from habits.paginations import HabitPaginator
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer
from habits.service import create_schedule, delete_schedule, update_schedule


class HabitCreateAPIView(generics.CreateAPIView):
    """Создание привычки"""

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_habit = serializer.save()
        new_habit.owner = self.request.user
        create_schedule(new_habit)
        new_habit.save()


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """Просмотр информации об одной привычке"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitUpdateAPIView(generics.UpdateAPIView):
    """Редактирование привычки"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_update(self, serializer):
        habit = serializer.save()
        update_schedule(habit)
        habit.save()


class HabitDestroyAPIView(generics.DestroyAPIView):
    """Удаление привычки"""

    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_destroy(self, instance):
        delete_schedule(instance)
        instance.delete()


class HabitListAPIView(generics.ListAPIView):
    """Вывод списка привычек пользователя"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        queryset = Habit.objects.filter(owner=self.request.user)
        return queryset


class HabitPublicListAPIView(generics.ListAPIView):
    """Вывод списка публичных привычек"""

    serializer_class = HabitSerializer
    pagination_class = HabitPaginator
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Habit.objects.filter(public_visibility=True)
        return queryset
