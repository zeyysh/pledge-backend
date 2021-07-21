from django.urls import path

from payment import views

urlpatterns = [
    path('', views.TransferList.as_view()),
    path('<int:pk>/', views.TransferDetail.as_view()),
]
