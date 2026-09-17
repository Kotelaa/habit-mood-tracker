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
    response = client.get('/api/habits/')
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_nonexistent_habit(auth_client):
    response = auth_client.get('/api/habits/99999/')
    assert response.status_code == 404


@pytest.mark.django_db
def test_update_habit(auth_client):
    create_response = auth_client.post('/api/habits/', {'name': 'Old name'})
    habit_id = create_response.data['id']

    update_response = auth_client.patch(f'/api/habits/{habit_id}/',
                                        {'name': 'New name'})
    assert update_response.status_code == 200
    assert update_response.data['name'] == 'New name'


@pytest.mark.django_db
def test_soft_delete_habit(auth_client):
    create_response = auth_client.post('/api/habits/',
                                       {'name': 'To be deleted'})
    habit_id = create_response.data['id']

    delete_response = auth_client.delete(f'/api/habits/{habit_id}/')
    assert delete_response.status_code == 204

    list_response = auth_client.get('/api/habits/')
    habit_ids = [h['id'] for h in list_response.data]
    assert habit_id not in habit_ids

    from habits.models import Habit
    habit = Habit.objects.get(id=habit_id)
    assert habit.is_deleted == True


@pytest.mark.django_db
def test_delete_habit_returns_204(habit):
    response = habit.soft_delete()
    assert response.status_code == 204


@pytest.mark.django_db
def test_delete_habit_exclude_from_list(habit):
    response = habit.soft_delete()
    habit_ids = [h for h in habit['id']]

    assert response.habit_id not in habit_ids


@pytest.mark.django_db
def test_delete_habit_is_deleted_True_in_db(habit):
    response = habit.soft_delete()
    assert response.data['is_deleted'] == True




@pytest.mark.django_db
def test_user_cannot_access_others_habits(auth_client, other_user):
    from habits.models import Habit
    other_habit = Habit.objects.create(user=other_user,
                                       name='Not shown habit')

    response = auth_client.get(f'/api/habits/{other_habit.id}/')
    assert response.status_code == 404


@pytest.mark.django_db
def test_filter_habits_by_name(auth_client):
    auth_client.post('/api/habits/', {'name': 'Read books'})
    auth_client.post('/api/habits/', {'name': 'Drink water'})

    response = auth_client.get('/api/habits/', {'search': 'water'})
    results = response.data['results'] if 'results' in response.data else response.data
    names = [h['name'] for h in results]

    assert 'Drink water' in names
    assert 'Read books' not in names


@pytest.mark.django_db
def test_update_habit_streak(auth_client):
    create_response = auth_client.post('/api/habits/', {'name': 'Do exercises'})
    habit_id = create_response.data['id']

    response = auth_client.patch(f'/api/habits/{habit_id}/', {'streak': 5})

    assert response.status_code == 200
    assert response.data['streak'] == 5
