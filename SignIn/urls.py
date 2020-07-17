"""
@author:      13716
@date-time:   2020/4/25-16:05
@ide:         PyCharm
@name:        urls.py
"""
from django.urls import path
from . import views
urlpatterns = [
    path("login/", views.LoginView.as_view()),
    path("sign/", views.SignView.as_view()),
    path("task/", views.TaskView.as_view()),
    path("get-task/", views.GetTaskView.as_view()),
    path("task-manager/", views.GetTaskManagerView.as_view())
]