from django.urls import path
from chatting import views

urlpatterns = [
    path('', views.ChatRoomView.as_view()),
]
