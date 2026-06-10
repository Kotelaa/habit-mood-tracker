from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ValidationError

from datetime import date

from .models import Habit, Mood


class HabitSerializer(ModelSerializer):

    class Meta:
        model = Habit
        fields = ['id', 'name', 'frequency', 'description',
                  'streak', 'last_completed', 'created_at']
        read_only_fields = ['id', 'streak', 'created_at']

    def validate_name(self, value: str):
        if len(value) < 3:
            raise ValidationError('Name must be at least 3 characters!')
        return value.capitalize()


class MoodSerializer(ModelSerializer):
    mood_display = serializers.CharField(source='get_mood_display', read_only=True)

    class Meta:
        model = Mood
        fields = ['id', 'mood', 'mood_display', 'note', 'date', 'created_at']
        read_only_fields = ['id', 'date', 'created_at']

    def validate(self, attrs):
        request = self.context.get('request')
        if request and request.method == 'POST':
            today = date.today()
            if Mood.objects.filter(user=request.user, date=today).exists():
                raise ValidationError('You already logged your mood today. Use'
                                      'PATCH to update it.')
        return attrs