import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from freezegun import freeze_time
from datetime import date

from habits.models import Habit

User = get_user_model()

@pytest.fixture
def user(db):
    return User.objects.create_user(username='TestUser', password='testpassword123')


@pytest.fixture
def auth_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def other_user(db):
    return User.objects.create_user(username='TestUser2', password='testpassword456')


@pytest.fixture
def anon_client():
    return APIClient()


@pytest.fixture
def created_habit(auth_client):
    response = auth_client.post('/api/habits/',
                                {'name': 'Created habit'})
    habit_id = response.data['id']
    return auth_client, habit_id


@pytest.fixture
def deleted_habit(auth_client):
    create_response = auth_client.post('/api/habits/', {'name': 'To be deleted'})
    habit_id = create_response.data['id']
    auth_client.delete(f'/api/habits/{habit_id}/')
    return habit_id


@pytest.fixture
def daily_habit_with_three_streaks(user):
    habit = Habit.objects.create(user=user, name='Daily habit with 3 streaks')

    with freeze_time("2026-07-15"):
        habit.complete()
    with freeze_time("2026-07-16"):
        habit.complete()
    with freeze_time("2026-07-17"):
        habit.complete()

    return habit


@pytest.fixture
def weekly_habit_with_two_streaks(user):
    habit = Habit.objects.create(user=user, name='Weekly habit with 2 streaks',
                                 frequency='weekly')

    with freeze_time("2026-07-16"):
        habit.complete()
    with freeze_time("2026-07-17"):
        habit.complete()

    return habit


@pytest.fixture
def monthly_habit_with_zero_streaks(user):
    habit = Habit.objects.create(user=user, name='Monthly habit with 0 streaks',
                                 frequency='monthly')
    return habit


@pytest.fixture
def created_mood(auth_client):
    response = auth_client.post('/api/mood/', {'mood': 3})
    mood_id = response.data['id']
    return auth_client, mood_id