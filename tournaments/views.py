from django.template.response import TemplateResponse

from general_src.base_view import BaseView


class TournamentMainView(BaseView):
    def get(self, request):
        return TemplateResponse(request, "tournaments_overview.html")
