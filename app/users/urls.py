# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.views import LogoutView
from django.urls import path

from users import views

urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('register/', views.register_user, name="register"),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path("logout/", LogoutView.as_view(), name="logout")
]
