import pytest

@pytest.mark.django_db
def test_mood_list_with_auth_client_returns_200(auth_client):
    response = auth_client.get('/api/mood/')
    assert response.status_code == 200