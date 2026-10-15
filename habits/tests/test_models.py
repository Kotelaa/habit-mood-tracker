import pytest
from django.contrib.auth import get_user_model
from freezegun import freeze_time
from datetime import date

from habits.models import Habit, Mood

User = get_user_model()

@pytest.mark.django_db
def test_habit_created_with_correct_fields(user):
    habit = Habit.objects.create(user=user, name='Drink water',
                                 description='Drink 8 glasses of water')
    assert habit.user == user
    assert habit.name == 'Drink water'
    assert habit.description == 'Drink 8 glasses of water'
    assert habit.streak == 0
    assert habit.frequency == 'daily'
    assert habit.is_deleted == False


@pytest.mark.django_db
def test_complete_habit_two_days_then_gap_resets_streak_to_one(user):
    habit = Habit.objects.create(user=user, name='Test streak')

    with freeze_time("2026-06-15"):
        habit.complete()

    with freeze_time("2026-06-16"):
        habit.complete()

    assert habit.streak == 2
    assert habit.last_completed == date(2026, 6, 16)

    with freeze_time("2026-06-18"):
        habit.complete()

    assert habit.streak == 1
    assert habit.last_completed == date(2026, 6, 18)


@pytest.mark.django_db
def test_complete_streak_three_days_in_a_row_returns_streak_three_and_last_data(user):
    habit = Habit.objects.create(user=user, name='Test streak')

    with freeze_time("2026-06-15"):
        habit.complete()

    with freeze_time("2026-06-16"):
        habit.complete()

    with freeze_time("2026-06-17"):
        habit.complete()

    assert habit.streak == 3
    assert habit.last_completed == date(2026, 6, 17)


@pytest.mark.django_db
def test_mood_created_with_corrected_fields(user):
    mood = Mood.objects.create(user=user, mood=2)

    assert mood.user == user
    assert mood.mood == 2