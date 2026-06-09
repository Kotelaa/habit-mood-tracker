from django.urls import path

from habits import views
from .mood_view import add_mood

urlpatterns = [
    path('', views.ListHabits.as_view(), name='habit_list'),
    path('habits/add/', views.CreateHabit.as_view(), name='add_habit'),
    path('habits/<int:habit_id>/', views.DetailHabit.as_view(),
         name='view_habit'),
    path('habits/delete/<int:habit_id>/', views.DeleteHabit.as_view(),
         name='delete_habit'),
    path('habits/edit/<int:habit_id>/', views.UpdateHabit.as_view(),
         name='edit_habit'),
    path('habits/complete/<int:habit_id>/', views.complete_habit,
         name='complete_habit'),

    path('add/mood/', add_mood, name='add_mood'),
]