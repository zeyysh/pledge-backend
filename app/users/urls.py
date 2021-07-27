# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path

from users import views

urlpatterns = [
    path('login/', views.LoginView, name="login"),
    path('login/<alt_method>', views.login_view_alt, name="login alt"),
    path('password_reset/request/{email}/', views.password_reset, name="password reset"),
    path('password_reset/new_pass', views.new_password, name="password reset"),
    path('current_user/', views.current_user, name="current_user"),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path('<int:pk>/', views.UserDetail.as_view()),
]
