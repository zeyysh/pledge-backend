# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.views import LogoutView
from django.urls import path

from users import views

urlpatterns = [
    # Matches any html file 
    path('login/', views.login_view, name="login"),
    path('register/', views.register_user, name="register"),
    # path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    # url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    path("logout/", LogoutView.as_view(), name="logout")
]
