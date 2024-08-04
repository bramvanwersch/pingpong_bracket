from django.urls import path

from scoreboard import views

urlpatterns = [
    path('', views.LandingPage.as_view()),
    path('add_score/', views.AddScoreView.as_view()),
]
