from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (ListView, DetailView, CreateView,
                                  UpdateView, DeleteView)
from django.urls import reverse_lazy, reverse

from .models import Habit
from .forms import HabitModelForm
from .mood_view import get_mood_context


class ListHabits(LoginRequiredMixin, ListView):
    model = Habit
    template_name = 'habits/habit_list.html'
    context_object_name = 'habits'

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user,
                                    is_deleted=False).order_by('-streak')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()
        context['greeting'] = f'Welcome, {self.request.user.username}!'
        context['total'] = qs.count()
        context['best'] = qs.first()

        context['daily_habits'] = qs.filter(frequency='daily')
        context['weekly_habits'] = qs.filter(frequency='weekly')
        context['monthly_habits'] = qs.filter(frequency='monthly')
        context['daily_count'] = context['daily_habits'].count()
        context['weekly_count'] = context['weekly_habits'].count()
        context['monthly_count'] = context['monthly_habits'].count()
        context.update(get_mood_context(self.request.user))
        return context


class DetailHabit(LoginRequiredMixin, DetailView):
    model = Habit
    template_name = 'habits/view_habit.html'
    context_object_name = 'habit'
    pk_url_kwarg = 'habit_id'

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class CreateHabit(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Habit
    form_class = HabitModelForm
    template_name = 'habits/add_habit.html'
    success_url = reverse_lazy('habit_list')
    success_message = "Habit '%(name)s' created successfully!"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_url'] = reverse_lazy('add_habit')
        context['submit_label'] = "Add habit"
        return context


class UpdateHabit(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Habit
    form_class = HabitModelForm
    template_name = 'habits/edit_habit.html'
    context_object_name = 'habit'
    success_message = "Habit '%(name)s' updated successfully!"
    pk_url_kwarg = 'habit_id'

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('view_habit', kwargs={'habit_id': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edit_url'] = reverse_lazy('edit_habit', kwargs={'habit_id': self.object.pk})
        context['submit_label'] = "Save changes!"
        return context


class DeleteHabit(LoginRequiredMixin, DeleteView):
    model = Habit
    template_name = 'habits/habit_confirm_delete.html'
    success_url = reverse_lazy('habit_list')
    pk_url_kwarg = 'habit_id'
    context_object_name = 'habit'

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def form_valid(self, form):
        self.object = self.get_object()
        self.object.soft_delete()
        messages.success(self.request, f'Habit \'{self.object.name}\' deleted successfully!')
        return super().form_valid(form)


@login_required
def complete_habit(request, habit_id):
    if request.method != 'POST':
        return redirect('habit_list')
    habit = get_object_or_404(Habit, user=request.user, id=habit_id)
    habit.complete()
    messages.success(request, f"{habit.name} completed.")
    return redirect("habit_list")