from django.urls import path
from chatting import consumers

websocket_urlpatterns = [
    path(r'ws/chatting/<str:chatname>', consumers.ChatConsumer.as_asgi())

]