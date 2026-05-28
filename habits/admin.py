from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ['name', 'streak', 'frequency', 'description']
    list_filter = ['streak', 'frequency', 'is_deleted']
    search_fields = ['name', 'description']
    ordering = ['-streak']
