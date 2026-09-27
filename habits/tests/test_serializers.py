import pytest
from habits.serializers import HabitSerializer

@pytest.mark.django_db
def test_habit_name_less_than_three_symbols_returns_validation_error():
    serializer = HabitSerializer(data={'name': 'ab'})
    assert serializer.is_valid() is False
    assert 'name' in serializer.errors


@pytest.mark.django_db
def test_habit_name_capitalized_on_save(user):
    serializer = HabitSerializer(data={'name': 'drink water'})
    assert serializer.is_valid() is True
    habit = serializer.save(user=user)
    assert habit.name == 'Drink water'


@pytest.mark.django_db
def test_patch_streak_field_is_ignored_stays_zero(created_habit):
    client, habit_id = created_habit
    response = client.patch(f'/api/habits/{habit_id}/', {'streak': 5})

    assert response.status_code == 200
    assert response.data['streak'] == 0