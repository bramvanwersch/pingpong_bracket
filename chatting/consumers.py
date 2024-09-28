import json
from datetime import datetime

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User

from chatting.models import ChatMessage, UserMessage

GENERAL_SESSION = 'general'


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        room_name = self.scope["url_route"]["kwargs"]["chatname"]
        self.session_id = f"{room_name}"

        await self.channel_layer.group_add(self.session_id, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.session_id,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        chat_message = await self._create_chat_message(message, username)
        await self.channel_layer.group_send(
            self.session_id, {
                "type": "send_message",
                "message": chat_message.message,
                "username": chat_message.sender.username,
                "date": chat_message.date
            })

    async def send_message(self, event):
        message = event["message"]
        username = event["username"]
        await self.send(text_data=json.dumps({"message": message, "username": username}))

    @database_sync_to_async
    def _create_chat_message(self, message: str, sender: str) -> ChatMessage:
        user = User.objects.get(username=sender)
        chat_message = ChatMessage.objects.create(message=message, sender=user, date=datetime.now())
        if self.session_id == GENERAL_SESSION:
            pass
        else:
            other_user = User.objects.get(username=self.session_id)
            UserMessage.objects.create(message=chat_message, message_read=False, user=other_user)
            UserMessage.objects.create(message=chat_message, message_read=True, user=user)
        return chat_message
