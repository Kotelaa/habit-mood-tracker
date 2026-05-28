from django.urls import path

from habits import views

urlpatterns = [
    path('', views.habit_list, name='habit_list'),
    path('habits/<int:habit_id>/', views.view_habit, name='view_habit'),
    path('habits/complete/<int:habit_id>/', views.complete_habit, name='complete_habit'),
    path('habits/add/', views.add_habit, name='add_habit'),
    path('habits/delete/<int:habit_id>/', views.delete_habit, name='delete_habit'),
    path('habits/edit/<int:habit_id>/', views.edit_habit, name='edit_habit')
]