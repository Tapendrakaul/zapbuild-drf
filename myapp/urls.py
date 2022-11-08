from .views import *
from django.urls import path


urlpatterns = [
    path('register',UserRegister.as_view()),
    path('login',LoginView.as_view()),

    path("task/", TaskView.as_view()),
    path("task/<id>/", TaskView.as_view()),
    path("task/<id>/assign-to/<pk>", TaskView.as_view()),
    
    path("tasks", TaskListView.as_view()),
    path("task-complete/<id>", TaskListView.as_view()),
    path("tasks-delete/<id>", DeleteTaskView.as_view()),
]