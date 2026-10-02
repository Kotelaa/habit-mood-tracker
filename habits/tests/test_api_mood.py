import pytest

@pytest.mark.django_db
def test_mood_list_with_auth_client_returns_200(auth_client):
    response = auth_client.get('/api/mood/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_mood_unauthenticated_client_returns_403(anon_client):
    response = anon_client.post('/api/mood/', {'mood': 2})
    assert response.status_code == 403