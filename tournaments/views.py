from django.template.response import TemplateResponse

from chatting.src import utility
from general_src.base_view import BaseView


class TournamentMainView(BaseView):
    def get(self, request):
        names = utility.get_user_mapping([request.user])

        return TemplateResponse(request, "tournaments_overview.html", {"names": names})


class CreateTournamentView(BaseView):
    def post(self, request):
        return TemplateResponse(request, "tournaments_detail.html")
