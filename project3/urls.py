from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('tasks/add/', views.add_task, name='task_add'),
    path('tasks/<int:task_id>/edit/', views.edit_task, name='task_edit'),
    path('tasks/<int:task_id>/done/', views.mark_done, name='task_done'),
    path('tasks/<int:task_id>/undone/', views.mark_undone, name='task_undone'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='task_delete'),
]
