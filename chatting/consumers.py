import datetime
import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User

from chatting.models import ChatMessage
from chatting.src import utility

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
        # if this is present we already have a message that needs to be relayed
        db_id = text_data_json["db_id"]
        user_id = text_data_json["user_id"]
        group = text_data_json["group_id"]
        if db_id is None:
            await self._create_chat_message(message, user_id, group)
        else:
            await self._send_existing(db_id, user_id, group)

    async def send_message(self, event):
        message = event["message"]
        username = event["username"]
        image_url = event["image_url"]
        date = event["date"]
        await self.send(
            text_data=json.dumps({"message": message, "username": username, "date": date, "image_url": image_url})
        )

    @database_sync_to_async
    def _create_chat_message(self, message: str, sender: str, group_id: str):
        sender = User.objects.get(pk=sender)
        chat_message = ChatMessage.objects.create(
            message=message, sender=sender, date=datetime.datetime.now(), chat_group_id=group_id
        )
        utility.send_message(chat_message, sender, group_id)

    @database_sync_to_async
    def _send_existing(self, db_id: str, sender: str, group_id: str):
        sender = User.objects.get(pk=sender)
        chat_message = ChatMessage.objects.get(pk=db_id)
        utility.send_message(chat_message, sender, group_id)
