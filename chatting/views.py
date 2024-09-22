from django.template.response import TemplateResponse
from django.views import View


class ChatRoomView(View):

    def get(self, request):
        return TemplateResponse(request, "chatroom.html")
