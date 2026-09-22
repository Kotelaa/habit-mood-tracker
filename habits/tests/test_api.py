import pytest
from datetime import date
from freezegun import freeze_time
from habits.models import Habit

@pytest.mark.django_db
def test_create_habit_returns_201_with_correct_name(auth_client):
    response = auth_client.post('/api/habits/', {'name': 'Read 10 pages'})
    assert response.status_code == 201
    assert response.data['name'] == 'Read 10 pages'


@pytest.mark.django_db
def test_list_habits_requires_auth_returns_403(anon_client):
    response = anon_client.get('/api/habits/')
    assert response.status_code == 403


@pytest.mark.django_db
def test_user_cannot_access_others_habits_returns_404(auth_client, other_user):
    other_habit = Habit.objects.create(user=other_user,
                                       name='Not shown habit')

    response = auth_client.get(f'/api/habits/{other_habit.id}/')
    assert response.status_code == 404


@pytest.mark.django_db
def test_get_nonexistent_habit_returns_404(auth_client):
    response = auth_client.get('/api/habits/99999/')
    assert response.status_code == 404


@pytest.mark.django_db
def test_update_habit_returns_200_and_updates_name(auth_client):
    create_response = auth_client.post('/api/habits/', {'name': 'Old name'})
    habit_id = create_response.data['id']

    update_response = auth_client.patch(f'/api/habits/{habit_id}/',
                                        {'name': 'New name'})
    assert update_response.status_code == 200
    assert update_response.data['name'] == 'New name'


@pytest.mark.django_db
def test_delete_habit_returns_204(created_habit):
    client, habit_id = created_habit
    response = client.delete(f'/api/habits/{habit_id}/')
    assert response.status_code == 204


@pytest.mark.django_db
def test_soft_deleted_habit_excluded_from_list(created_habit):
    client, habit_id = created_habit
    client.delete(f'/api/habits/{habit_id}/')

    list_response = client.get('/api/habits/')
    habit_ids = [h['id'] for h in list_response.data]

    assert habit_id not in habit_ids


@pytest.mark.django_db
def test_soft_deleted_habit_still_exists_in_db_as_deleted(created_habit):
    client, habit_id = created_habit
    client.delete(f'/api/habits/{habit_id}/')

    habit = Habit.objects.get(id=habit_id)
    assert habit.is_deleted == True



@pytest.mark.django_db
def test_complete_habit_increments_streak_by_one(created_habit):
    client, habit_id = created_habit
    response = client.post(f'/api/habits/{habit_id}/complete/')
    assert response.status_code == 200
    assert response.data['streak'] == 1



@pytest.mark.django_db
def test_search_habits_by_name_returns_matching_only(auth_client):
    auth_client.post('/api/habits/', {'name': 'Read books'})
    auth_client.post('/api/habits/', {'name': 'Drink water'})

    response = auth_client.get('/api/habits/', {'search': 'water'})
    results = response.data['results'] if 'results' in response.data else response.data
    names = [h['name'] for h in results]

    assert 'Drink water' in names
    assert 'Read books' not in names


@pytest.mark.django_db
def test_patch_streak_field_is_ignored_stays_zero(created_habit):
    client, habit_id = created_habit
    response = client.patch(f'/api/habits/{habit_id}/', {'streak': 5})

    assert response.status_code == 200
    assert response.data['streak'] == 0


@pytest.mark.django_db
def test_complete_habit_three_times_skipping_one_day_still_increments_streak(user):
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



