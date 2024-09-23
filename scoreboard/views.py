import datetime
import uuid

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from general_src.base_view import BaseView
from login.models import UserData
from scoreboard.models import MatchResult
from scoreboard.src.score import record_score
from scoreboard.src.utility import get_rating_data


class LandingPage(BaseView):

    def get(self, request):
        names = {u.username for u in User.objects.all()}
        names.remove(request.user.username)
        data = get_rating_data(MatchResult.objects.all().order_by("-date"))
        return TemplateResponse(request, "landingpage.html", {"names": sorted(names, key=lambda x: x.lower()), "matches": data, "current": 'home'})


class AddScoreView(BaseView):

    def post(self, request):
        data = request.POST
        p1_data = UserData.objects.get(user=request.user)
        p2_data = UserData.objects.get(user__username=data["oponent"])
        p1_score = data["my_points"]
        p2_score = data["oponent_points"]
        if p1_score == '' or p2_score == '':
            return HttpResponseRedirect('/')
        match_id = uuid.uuid4()
        score_player = MatchResult.objects.create(player=request.user, opponent=p2_data.user, player_score=p1_score,
                                                  opponents_score=p2_score, date=datetime.datetime.now(),
                                                  rate_change=0.0, match_id=match_id)
        record_score(p1_data, p2_data, score_player)
        MatchResult.objects.create(player=p2_data.user, opponent=request.user, player_score=p2_score,
                                   opponents_score=p1_score, date=datetime.datetime.now(),
                                   rate_change=-1 * score_player.rate_change, match_id=match_id)
        return HttpResponseRedirect('/')
