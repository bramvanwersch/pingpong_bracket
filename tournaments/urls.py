from django.urls import path

from tournaments import views

urlpatterns = [
    path("", views.TournamentMainView.as_view()),
    path("detail/<str:tournament_id>", views.TournamentDetailView.as_view()),
    path("create", views.CreateTournamentView.as_view()),
    path("leave/<str:tournament_id>", views.LeaveTournamentView.as_view()),
    path("join/<str:tournament_id>", views.JoinTournamentView.as_view()),
    path("start/<str:tournament_id>", views.StartTournamentView.as_view()),
    path("delete/<str:tournament_id>", views.DeleteTournamentView.as_view()),
]
