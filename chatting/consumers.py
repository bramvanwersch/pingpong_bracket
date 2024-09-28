import json
from datetime import datetime

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User

from chatting.models import ChatGroupUser, ChatMessage, UserMessage

GENERAL_SESSION = "general"


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        room_name = self.scope["url_route"]["kwargs"]["chatname"]
        self.session_id = f"{room_name}"

        await self.channel_layer.group_add(self.session_id, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.session_id, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user_id = text_data_json["user_id"]
        group = text_data_json["group_id"]
        chat_message = await self._create_chat_message(message, user_id, group)
        await self.channel_layer.group_send(
            self.session_id,
            {
                "type": "send_message",
                "message": chat_message.message,
                "username": chat_message.sender.username,
                "date": chat_message.date.strftime("%Y-%m-%d %H:%M:%S"),
            },
        )

    async def send_message(self, event):
        message = event["message"]
        username = event["username"]
        date = event["date"]
        await self.send(text_data=json.dumps({"message": message, "username": username, "date": date}))

    @database_sync_to_async
    def _create_chat_message(self, message: str, sender: str, group_id: str) -> ChatMessage:
        sender = User.objects.get(pk=sender)
        other_users = [cgu.user_id for cgu in ChatGroupUser.objects.filter(group_id=group_id)]
        chat_message = ChatMessage.objects.create(
            message=message, sender=sender, date=datetime.now(), chat_group_id=group_id
        )
        if self.session_id == GENERAL_SESSION:
            pass
        else:
            UserMessage.objects.create(message=chat_message, message_read=True, user=sender)
            for user_id in other_users:
                UserMessage.objects.create(message=chat_message, message_read=True, user_id=user_id)
        return chat_message
