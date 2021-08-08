from django.urls import path

from user_verification import views

urlpatterns = [
    path('verification/', views.VerificationList.as_view()),
    path('verification/<int:pk>/', views.VerificationDetail.as_view()),
]
