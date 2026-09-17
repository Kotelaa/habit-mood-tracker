import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

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
def habit(auth_client):
    response = auth_client.post('/api/habits/',
                                {'name': 'Example habit'})
    habit_id = response.data['id']
    return habit, habit_id