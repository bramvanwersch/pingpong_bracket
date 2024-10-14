from django.urls import path

from tournaments import views

urlpatterns = [
    path("", views.TournamentMainView.as_view()),
    path("create", views.TournamentMainView.as_view()),
]
