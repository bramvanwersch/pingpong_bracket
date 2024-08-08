from typing import Dict, Any

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from general_src.base_view import BaseView
from login.models import UserData
from login.src.utility import get_player_data, get_comparative_player_data
from scoreboard.models import Scores
from scoreboard.src.utility import get_player_rating_data


class LeaderboardView(BaseView):

    def get(self, request):
        player_data = sorted(get_player_data(UserData.objects.all().prefetch_related("user")), key=self.__sort_rating, reverse=True)
        return TemplateResponse(request, "leaderboard.html", {"players": player_data, "current": "leaderboard"})

    def __sort_rating(self, rating_dct: Dict[str, Any]) -> int:
        if isinstance(rating_dct["rating"], str):
            return 0
        return rating_dct["rating"]


class LeaderboardDetailView(BaseView):

    def get(self, request, name: str):
        profile = get_player_data([UserData.objects.get(user__username=name)])[0]
        user = User.objects.get(username=name)
        matches = sorted(get_player_rating_data(Scores.get_player_scores(user)[:50], user), key=lambda x: x["date"], reverse=True)
        names = {u.username for u in User.objects.all()}
        names.remove(name)
        if user == request.user:
            current = "my_profile"
        else:
            current = "leaderboard"
        return TemplateResponse(request, "leaderboard_personal.html",
                                {"profile": profile, "current": current, "matches": matches, "names": names})


class LeaderboardCompareView(BaseView):

    def get(self, request, name: str, other_name: str):
        user = User.objects.get(username=name)
        other_user = User.objects.get(username=other_name)
        matches = sorted(get_player_rating_data(Scores.get_player_scores(user, other_user)[:50], user), key=lambda x: x["date"], reverse=True)
        profile, other_profile = get_comparative_player_data(user, other_user)
        if user == request.user:
            current = "my_profile"
        else:
            current = "leaderboard"
        return TemplateResponse(request, "leaderboard_compare.html",
                                {"profile": profile, "other_profile": other_profile, "current": current, "matches": matches})


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
