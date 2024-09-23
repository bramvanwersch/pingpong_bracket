from django.urls import path
from chatting import views

urlpatterns = [
    path('', views.ChatRoomView.as_view()),
    path('<str:room_name>', views.ChatRoomView.as_view()),
]
