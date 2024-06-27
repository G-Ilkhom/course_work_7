from django.urls import path

from habits.apps import HabitsConfig
from habits.views import HabitListAPIView

app_name = HabitsConfig.name

urlpatterns = [
    path('', HabitListAPIView.as_view(), name='habit_list'),
]
