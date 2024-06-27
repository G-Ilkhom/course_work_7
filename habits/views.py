from django.shortcuts import render
from rest_framework import generics
from habits.models import Habit


class HabitListAPIView(generics.ListAPIView):
    """ Вывод привычек пользователя """

    queryset = Habit.objects.all()
    