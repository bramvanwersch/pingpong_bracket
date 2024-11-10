from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from chatting.src.utility import get_user_mapping
from general_src.base_view import BaseView
from login.models import UserData
from scoreboard.models import MatchResult
from scoreboard.src.score import record_match_results
from scoreboard.src.utility import get_rating_data


class LandingPage(BaseView):
    def get(self, request):
        names = list(get_user_mapping([request.user]).keys())
        data = get_rating_data(MatchResult.objects.all().order_by("-date"))
        return TemplateResponse(
            request,
            "landingpage.html",
            {"names": sorted(names, key=lambda x: x.lower()), "matches": data, "current": "home"},
        )


class AddScoreView(BaseView):
    def post(self, request):
        data = request.POST
        p1_data = UserData.objects.get(user=request.user)
        p2_data = UserData.objects.get(user__username=data["oponent"])
        p1_score = data["my_points"]
        p2_score = data["oponent_points"]
        if p1_score == "" or p2_score == "":
            return HttpResponseRedirect("/")
        record_match_results(p1_data, p2_data, p1_score, p2_score)
        return HttpResponseRedirect("/")
