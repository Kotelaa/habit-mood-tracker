from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages
from datetime import date

from .models import Mood
from .forms import MoodForm

@login_required
def add_mood(request):
    today = date.today()
    existing = Mood.objects.filter(user=request.user, date=today).first()
    if request.method == 'POST':
        form = MoodForm(request.POST, instance=existing)

        if form.is_valid():
            mood = form.save(commit=False)
            mood.user = request.user
            mood.save()
            messages.success(request, 'Mood logged successfully!')
        else:
            messages.error(request, 'Invalid mood entry.')

    return redirect('habit_list')


def get_mood_context(user):
    today = date.today()
    return {
        'today_mood': Mood.objects.filter(user=user, date=today).first(),
        'mood_form': MoodForm(),
        'recent_moods': Mood.objects.filter(user=user)[:7]
    }