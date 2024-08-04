from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from general_src.base_view import BaseView
from login.models import UserData
from login.src.utility import get_player_data
from scoreboard.models import Scores
from scoreboard.src.utility import get_rating_data


class LeaderboardView(BaseView):

    def get(self, request):
        player_data = get_player_data(UserData.objects.all().prefetch_related("user").order_by("-rating"))
        return TemplateResponse(request, "leaderboard.html", {"players": player_data, "current": "leaderboard"})


class LeaderboardDetailView(BaseView):

    def get(self, request, name: str):
        profile = get_player_data([UserData.objects.get(user__username=name)])[0]
        user = User.objects.get(username=name)
        matches = get_rating_data(list(Scores.objects.filter(player1=user)) + list(Scores.objects.filter(player2=user)), False)
        if user == request.user:
            return TemplateResponse(request, "leaderboard_own.html",
                                    {"profile": profile, "current": "my_profile", "matches": matches})
        own_profile = get_player_data([UserData.objects.get(user=request.user)])[0]
        return TemplateResponse(request, "leaderboard_detail.html", {"profile": profile, "current": "leaderboard", "matches": matches, "my": own_profile})


class LeaderboardDeleteView(BaseView):

    def get(self, request, db_id: str):
        score = Scores.objects.get(id=db_id)
        user_data1 = UserData.objects.get(user=score.player1)
        user_data2 = UserData.objects.get(user=score.player2)
        if score.p1_score > score.p2_score:
            user_data1.wins -= 1
            user_data2.losses -= 1
        elif score.p2_score > score.p1_score:
            user_data1.losses -= 1
            user_data2.wins -= 1
        else:
            user_data1.ties -= 1
            user_data2.ties -= 1
        user_data1.rating -= score.p1_rate_change
        user_data2.rating -= score.p2_rate_change
        user_data1.save()
        user_data2.save()
        score.delete()
        return HttpResponseRedirect(f'/leaderboard/{request.user.username}')
