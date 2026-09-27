import pytest
from habits.serializers import HabitSerializer

@pytest.mark.django_db
def test_habit_name_less_than_three_symbols_returns_validation_error():
    serializer = HabitSerializer(data={'name': 'ab'})
    assert serializer.is_valid() is False
    assert 'name' in serializer.errors