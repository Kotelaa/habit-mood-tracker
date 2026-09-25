import pytest
from django.contrib.auth import get_user_model
from freezegun import freeze_time
from datetime import date

from habits.models import Habit, Mood

User = get_user_model()

@pytest.mark.django_db
def test_habit_created_with_correct_fields():
    user = User.objects.create_user(username='TestUser', password='testpassword123')
    habit = Habit.objects.create(user=user, name='Drink water',
                                 description='Drink 8 glasses of water')
    assert habit.user == user
    assert habit.name == 'Drink water'
    assert habit.description == 'Drink 8 glasses of water'
    assert habit.streak == 0
    assert habit.frequency == 'daily'
    assert habit.is_deleted == False


@pytest.mark.django_db
def test_mood_created_with_corrected_fields():
    user = User.objects.create(username='TestUser', password='testpassword123')
    mood = Mood.objects.create(user=user, mood=2)

    assert mood.user == user
    assert mood.mood == 2