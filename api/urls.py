from django.urls import path

from chatting import api as chatting_api
from login import api as login_api

urlpatterns = [
    path("chatting/get_nr_messages", chatting_api.NumberNotificationsView.as_view()),
    path("login/upload_image", login_api.UploadLoginImage.as_view()),
]
