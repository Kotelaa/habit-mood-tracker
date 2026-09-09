import pytest

@pytest.mark.django_db
def test_create_habit(auth_client):
    response = auth_client.post('/api/habits/', {'name': 'Read 10 pages'})
    assert response.status_code == 201
    assert response.data['name'] == 'Read 10 pages'


@pytest.mark.django_db
def test_list_habits_requires_auth():
    from rest_framework.test import APIClient
    client = APIClient()
    response = client.get('/api/habits')
    assert response.status_code == 401


@pytest.mark.django_db
def test_get_nonexistent_habit(auth_client):
    response = auth_client.get('/api/habits/99999')
    assert response.status_code == 404


@pytest.mark.django_db
def test_update_habit(auth_client):
    response = auth_client.post('/api/habits/', {'name': 'Old name'})
    habit_id = create_response.data['id']

    update_response = auth_client.patch(f'/api/habits/{habit_id}',
                                        {'name': 'New name'})
    assert update_response.status_code == 200
    assert update_response.data['name'] == 'New name'