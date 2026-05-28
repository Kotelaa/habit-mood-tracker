from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .models import Habit
from .forms import HabitModelForm, RegisterForm


@login_required
def habit_list(request):
    habits = Habit.objects.filter(user=request.user, is_deleted=False).order_by('-streak')
    return render(request, 'habits/habit_list.html',
                  {'habits': habits})


@login_required
def view_habit(request, habit_id):
    habit = get_object_or_404(Habit, user=request.user, id=habit_id)
    return render(request, 'habits/view_habit.html',
                  {'habit': habit})


@login_required
def add_habit(request):
    if request.method == "POST":
        form = HabitModelForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            messages.success(request, f'Your habit \'{habit.name}\' added!')
            return redirect('habit_list')
    else:
        form = HabitModelForm()
    return render(request, 'habits/add_habit.html',
                  {'form': form,
                   'add_url': reverse('add_habit')})


@login_required
def edit_habit(request, habit_id):
    habit = get_object_or_404(Habit, user=request.user, id=habit_id)
    if request.method == 'POST':
        form = HabitModelForm(request.POST, instance=habit)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            messages.success(request, f'Your habit \'{habit.name}\' changed!')
            return redirect('view_habit', habit_id=habit.id)
    else:
        form = HabitModelForm(instance=habit)
    return render(request, 'habits/edit_habit.html',
                  {'form': form,
                   'habit': 'habit',
                   'edit_url': reverse('edit_habit', args=[habit_id])})


@login_required
def complete_habit(request, habit_id):
    habit = get_object_or_404(Habit, user=request.user, id=habit_id)
    habit.complete()
    messages.success(request, f"{habit.name} completed.")
    return redirect("habit_list")


@login_required
def delete_habit(request, habit_id):
    habit = get_object_or_404(Habit, user=request.user, id=habit_id)
    habit.soft_delete()
    messages.success(request, f"{habit.name} deleted.")
    return redirect("habit_list")


def register(request):
    if request.user.is_authenticated:
        return redirect('habit_list')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Hello, {user.username}')
            return redirect('habit_list')
    else:
        form = RegisterForm()

    return render(request, 'auth/register.html',
                  {'form': form,
                   'registration_url': reverse('register')})




