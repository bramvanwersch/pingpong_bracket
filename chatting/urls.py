from django.urls import path

from chatting import views

urlpatterns = [
    path("", views.ChatRoomView.as_view()),
    path("new/<str:user_ids>", views.NewChatRoomView.as_view()),
    path("<str:group_id>", views.ChatRoomView.as_view()),
]
