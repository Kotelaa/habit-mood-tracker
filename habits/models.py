from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models

from datetime import date

class Habit(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='habits')
    name = models.CharField(max_length=150)
    streak = models.IntegerField(default=0)
    frequency = models.CharField(max_length=20,
                                 choices=FREQUENCY_CHOICES,
                                 default='daily')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_completed = models.DateField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-streak']
        verbose_name_plural = 'habits'

    def __str__(self):
        return f"{self.name} | Streak: {self.streak}"

    def complete(self):
        self.streak += 1
        self.last_completed = date.today()
        self.save()

    def soft_delete(self):
        self.is_deleted = True
        self.save()


class Mood(models.Model):
    MOOD_CHOICES = [
        (5, '😄 Great'),
        (4, '🙂 Good'),
        (3, '😐 Okay'),
        (2, '😕 Low'),
        (1, '😞 Bad'),
    ]
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='moods')
    mood = models.IntegerField(choices=MOOD_CHOICES,
                               default=4)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = (('user', 'mood'),)

        def __str__(self):
            return (f'{self.user.username} | {self.get_mood_display()} | '
                    f'Note: {self.note} | Date: {self.date}')
