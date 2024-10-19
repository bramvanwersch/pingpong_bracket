from django.urls import path

from chatting import api as chatting_api
from login import api as login_api
from tournaments import api as tournament_api

urlpatterns = [
    path("chatting/get_nr_messages", chatting_api.NumberNotificationsView.as_view()),
    path("chatting/send_image/<str:group_id>", chatting_api.SendImage.as_view()),
    path("login/upload_image", login_api.UploadLoginImage.as_view()),
    path("login/get_image", login_api.GetProfileImage.as_view()),
    path("tournament/add_score/<str:db_id>", tournament_api.SetGameScore.as_view()),
]
