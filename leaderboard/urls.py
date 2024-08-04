from django.urls import path

from leaderboard import views

urlpatterns = [
    path('', views.LeaderboardView.as_view()),
    path('<str:name>/', views.LeaderboardDetailView.as_view()),
    path('delete/<str:db_id>/', views.LeaderboardDeleteView.as_view()),
]
