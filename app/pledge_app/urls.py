from django.urls import path

from pledge_app import views

urlpatterns = [
    path('', views.PledgeList.as_view()),
    path('<int:pk>/', views.PledgeDetail.as_view()),
]
