from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'place', 'time', 'action', 'pleasant_habit', 'linked_habit', 'periodicity', 'reward',
                    'time_required', 'public_visibility',)
    list_filter = ('owner',)
    search_fields = ('owner', 'action')
