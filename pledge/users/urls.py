from django.conf.urls import url
from django.contrib.auth.views import LogoutView
from django.urls import path
from rest_framework.authtoken import views as authviews

from users import views

urlpatterns = [
    # Matches any html file
    path('login/', views.login_view, name="login"),
    path('register/', views.register_user, name="register"),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path("logout/", LogoutView.as_view(), name="logout"),
    url(r'^api-token-auth/', authviews.obtain_auth_token),

]
