import pytest

@pytest.mark.django_db
def test_mood_list_with_auth_client_returns_200(auth_client):
    response = auth_client.get('/api/mood/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_mood_unauthenticated_client_returns_403(anon_client):
    response = anon_client.post('/api/mood/', {'mood': 2})
    assert response.status_code == 403


@pytest.mark.django_db
def test_create_mood_returns_201_and_correct_mood(auth_client):
    response = auth_client.post('/api/mood/', {'mood': 4})
    assert response.status_code == 201
    assert response.data['mood'] == 4
    assert response.data['mood_display'] == '🙂 Good'


@pytest.mark.django_db
def test_mood_list_for_auth_user_returns_200_and_all_moods(auth_client):
    auth_client.post('/api/mood/', {'mood': 5})
    response = auth_client.get('/api/mood/')
    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_mood_update_returns_200_and_new_mood(auth_client):
    create_response = auth_client.post('/api/mood/', {'mood': 2})
    mood_id = create_response.data['id']

    response = auth_client.patch(f'/api/mood/{mood_id}/', {'mood': 4})
    assert response.status_code == 200
    assert response.data['mood'] == 4


@pytest.mark.django_db
def test_create_second_mood_same_day_returns_400(auth_client):
    auth_client.post('/api/mood/', {'mood': 1})
    response = auth_client.post('/api/mood/', {'mood': 3})
    assert response.status_code == 400