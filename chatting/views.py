from django.contrib.auth.models import User
from django.template.response import TemplateResponse
from django.views import View


class ChatRoomView(View):

    def get(self, request, room_name: str = "general"):
        names = {u.username for u in User.objects.all()}
        names.remove(request.user.username)
        return TemplateResponse(request, "chatroom.html",
                                {"current": "chatting", "names": sorted(names, key=lambda x: x.lower()), "room_name": room_name})
