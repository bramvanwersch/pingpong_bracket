from django.contrib.auth.models import User
from django.db.models.functions import Lower
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views import View

from chatting.models import ChatGroup, ChatMessage
from chatting.src import utility


class ChatRoomView(View):
    def get(self, request, group_id: int = None):
        names = utility.get_user_mapping([request.user])
        group_names = utility.get_group_mapping(request.user)
        messages = ChatMessage.objects.filter(chat_group_id=group_id).order_by("date")
        formatted_messages = []
        for message in messages:
            formatted_messages.append(
                {
                    "message": message.message,
                    "username": message.sender.username,
                    "date": message.date.strftime("%Y-%m-%d %H:%M:%S"),
                }
            )
        return TemplateResponse(
            request,
            "chatroom.html",
            {
                "current": "chatting",
                "names": names,
                "group_id": group_id,
                "group_names": group_names,
                "messages": formatted_messages,
            },
        )


class NewChatRoomView(View):
    def get(self, request, user_ids):
        ids = user_ids.split(";")
        users = User.objects.filter(pk__in=ids).order_by(Lower("username"))
        group = ChatGroup.create_or_get_group(request.user, list(users))
        return redirect(f"/chatroom/{group.pk}")


class ChatChallengeView(View):
    def get(self, request, user_name: str):
        challenge_user = User.objects.get(username=user_name)
        group = ChatGroup.create_or_get_group(request.user, [challenge_user])
        utility.send_message(f"{request.user.username} challenges you to a match!", request.user, f"{group.id}")
        return redirect(f"/chatroom/{group.pk}")
