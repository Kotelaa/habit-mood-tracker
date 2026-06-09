from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.urls import reverse_lazy

from .forms import RegisterForm

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