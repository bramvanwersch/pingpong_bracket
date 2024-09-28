from django.urls import path

from matchmaking import views

urlpatterns = [
    path("", views.MatchmakingView.as_view()),
    path("add_match_request/", views.AddMatchRequest.as_view()),
    path("delete_request/<str:db_id>", views.DeleteMatchRequest.as_view()),
    path("accept_request/<str:db_id>", views.AcceptRequest.as_view()),
    path("retract_request/<str:db_id>", views.RetractRequest.as_view()),
    path("challenge/<str:name>", views.ChallengeRequest.as_view()),
]
