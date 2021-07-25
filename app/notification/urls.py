from django.urls import path

from notification import views

urlpatterns = [
    path('zey/', views.MyTestAPIView.as_view()),
    path('<int:pk>/', views.NotificationDetail.as_view()),
]
