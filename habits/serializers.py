from rest_framework.serializers import ModelSerializer, ValidationError

from .models import Habit


class HabitSerializer (ModelSerializer):

    class Meta:
        model = Habit
        fields = ['id', 'name', 'frequency', 'description',
                  'streak', 'last_completed', 'created_at']
        read_only_fields = ['id', 'streak', 'created_at']

    def validate_name(self, value: str):
        if len(value) < 3:
            raise ValidationError('Name must be at least 3 characters!')
        return value.capitalize()
