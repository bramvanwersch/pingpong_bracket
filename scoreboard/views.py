import datetime

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from general_src.base_view import BaseView
from login.models import UserData
from scoreboard.models import Scores
from scoreboard.src.score import record_score
from scoreboard.src.utility import get_rating_data


class LandingPage(BaseView):

    def get(self, request):
        names = {u.username for u in User.objects.all()}
        names.remove(request.user.username)
        data = get_rating_data(Scores.objects.all().order_by("-date")[:25])
        return TemplateResponse(request, "landingpage.html", {"names": list(names), "matches": data, "current": 'home'})


class AddScoreView(BaseView):

    def post(self, request):
        data = request.POST
        p1_data = UserData.objects.get(user=request.user)
        p2_data = UserData.objects.get(user__username=data["oponent"])
        p1_score = data["my_points"]
        p2_score = data["oponent_points"]
        # meho
        if p1_score == '' or p2_score == '':
            return HttpResponseRedirect('/')
        score_record = Scores.objects.create(player1=request.user, player2=p2_data.user, p1_score=p1_score,
                                             p2_score=p2_score, date=datetime.datetime.now())
        record_score(p1_data, p2_data, score_record)
        return HttpResponseRedirect('/')
