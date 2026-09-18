import pytest

@pytest.mark.django_db
def test_create_habit_returns_201(auth_client):
    response = auth_client.post('/api/habits/', {'name': 'Read 10 pages'})
    assert response.status_code == 201
    assert response.data['name'] == 'Read 10 pages'


@pytest.mark.django_db
def test_list_habits_requires_auth_returns_403():
    from rest_framework.test import APIClient
    client = APIClient()
    response = client.get('/api/habits/')
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_nonexistent_habit_returns_404(auth_client):
    response = auth_client.get('/api/habits/99999/')
    assert response.status_code == 404


@pytest.mark.django_db
def test_update_habit_returns_200(auth_client):
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
    response = habit[0].soft_delete()
    assert response.status_code == 204


@pytest.mark.django_db
def test_delete_habit_exclude_from_list(habit):
    response = habit[0].soft_delete()
    habit_ids = [h for h in habit['id']]

    assert response.habit_id not in habit_ids


@pytest.mark.django_db
def test_delete_habit_is_deleted_True_in_db(habit):
    response = habit[0].soft_delete()
    assert response.data['is_deleted'] == True


@pytest.mark.django_db
def test_habit_complete_returns_streak_1(habit):
    response = habit[0].complete()
    assert habit[0].streak == 1


@pytest.mark.django_db
def test_user_cannot_access_others_habits_returns_404(auth_client, other_user):
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
def test_patch_streak_directly_is_ignored(auth_client):
    create_response = auth_client.post('/api/habits/', {'name': 'Do exercises'})
    habit_id = create_response.data['id']

    response = auth_client.patch(f'/api/habits/{habit_id}/', {'streak': 5})

    assert response.status_code == 200
    assert response.data['streak'] == 0


def test_increase_streak_3_days_in_a_row(auth_client):
    habit = auth_client.post(name='Test')

    with freeze_time("2026-06-15"):
        habit.complete()

    with freeze_time("2026-06-16"):
        habit.complete()

    with freeze_time("2026-06-18"):
        habit.complete()

    assert habit.streak == 3
    assert habit.last_completed == date(2026, 6, 18)



