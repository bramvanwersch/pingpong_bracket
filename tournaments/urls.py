from django.urls import path

from tournaments import views

urlpatterns = [
    path("", views.TournamentMainView.as_view()),
    path("detail/<str:tournament_id>", views.TournamentDetailView.as_view()),
    path("create", views.CreateTournamentView.as_view()),
]
