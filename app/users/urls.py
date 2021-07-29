# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path

from users import views

urlpatterns = [
    path('user/', views.UserList.as_view()),
    path('<int:pk>/', views.UserDetail.as_view()),
]
