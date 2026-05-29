from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (ListView, DetailView, CreateView,
                                  UpdateView, DeleteView)
from django.urls import reverse_lazy, reverse

from .models import Habit
from .forms import HabitModelForm, RegisterForm


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
                   'registration_url': reverse_lazy('register')})



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
    success_message = "Habit '%(name)s' created successfully!'"

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
        return reverse_lazy('edit_habit', kwargs={'habit_id': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edit_url'] = reverse_lazy('edit_habit', kwargs={'habit_id': self.object.pk})
        context['submit_label'] = "Save changes!"
        return context


class DeleteHabit(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Habit
    template_name = 'habits/habit_confirm_delete.html'
    success_url = reverse_lazy('habit_list')
    pk_url_kwarg = 'habit_id'
    context_object_name = 'habit'

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, f'Habit \'{self.object.name}\' deleted successfully!')
        return super().form_valid(form)


@login_required
def complete_habit(request, habit_id):
    habit = get_object_or_404(Habit, user=request.user, id=habit_id)
    habit.complete()
    messages.success(request, f"{habit.name} completed.")
    return redirect("habit_list")