import json, os

FILENAME = 'habits.json'

def load_habits():
    if os.path.exists(FILENAME):
        with open(FILENAME, 'r') as f:
            return json.load(f)
    return {}

def save_habits(habits):
    with open(FILENAME, 'w') as f:
        json.dump(habits, f, indent=4)

def add_habit():
    habits = load_habits()

    habit_name = input('Enter habit name: ')
    if habit_name in habits:
        print(f'You already have habit with name: {habit_name}')
        return
    else:
        habits[habit_name] = {'streak': 0}
        save_habits(habits)

def complete_habit(habits):
    habit_name = input('Enter habit name: ')

    if habit_name in habits:
        habits[habit_name]['streak'] += 1
        save_habits(habits)
    else:
        print(f'You don\'t have habit with name: {habit_name}')
        return

def show_stats():
    habits = load_habits()

    if not habits:
        print('No habits')
        return
    for habit, stats in habits.items():
        print(f'{habit} streak: {stats["streak"]}')




