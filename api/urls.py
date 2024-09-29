from django.urls import path

from chatting import api

urlpatterns = [
    path("chatting/get_nr_messages", api.NumberNotificationsView.as_view()),
]
