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




# class Profile(models.Model):
#     user       = models.OneToOneField(User, on_delete=models.CASCADE)
#     bio        = models.TextField(blank=True)
#     timezone   = models.CharField(max_length=50, default="UTC")
#
#     def __str__(self):
#         return f"{self.user.username}'s profile"
#
#
#     @receiver(post_save, sender=User)
#     def create_profile(sender, instance, created, **kwargs):
#         if created:
#             Profile.objects.create(user=instance)
#
#     @receiver(post_save, sender=User)
#     def save_profile(sender, instance, **kwargs):
#         instance.profile.save()