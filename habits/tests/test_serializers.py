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
def test_habit_id_field_read_only_and_cannot_be_changed():
    serializer = HabitSerializer(data={'name': 'Test habit', 'id': 999})
    assert serializer.is_valid() is True
    assert 'id' not in serializer.validated_data