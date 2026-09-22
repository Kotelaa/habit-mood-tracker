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
def anon_client():
    return APIClient()


@pytest.fixture
def created_habit(auth_client):
    response = auth_client.post('/api/habits/',
                                {'name': 'Example habit'})
    habit_id = response.data['id']
    return auth_client, habit_id


@pytest.fixture
def deleted_habit(auth_client):
    create_response = auth_client.post('/api/habits/', {'name': 'To be deleted'})
    habit_id = create_response.data['id']
    auth_client.delete(f'/api/habits/{habit_id}/')
    return habit_id
