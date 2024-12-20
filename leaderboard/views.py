from typing import Any, Dict, List, Tuple

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from chatting.src.utility import get_user_mapping
from general_src.base_view import BaseView
from login.models import UserData
from login.src.utility import get_comparative_player_data, get_player_data
from scoreboard.models import MatchResult, Result
from scoreboard.src.utility import get_player_rating_data
from tournaments.models import TournamentGame


class LeaderboardView(BaseView):
    def get(self, request):
        player_data = sorted(
            get_player_data(UserData.objects.all().prefetch_related("user")), key=self.__sort_rating, reverse=True
        )
        return TemplateResponse(request, "leaderboard.html", {"players": player_data, "current": "leaderboard"})

    def __sort_rating(self, rating_dct: Dict[str, Any]) -> int:
        if isinstance(rating_dct["rating"], str):
            return 0
        return rating_dct["rating"]


class LeaderboardDetailView(BaseView):
    def get(self, request, name: str):
        profile = get_player_data([UserData.objects.get(user__username=name)])[0]
        user = User.objects.get(username=name)
        matches = sorted(
            get_player_rating_data(MatchResult.get_player_scores(user)[:50]), key=lambda x: x["date"], reverse=True
        )
        names = list(get_user_mapping([request.user]).keys())
        ratings, labels = self._get_match_line_data(user)
        if user == request.user:
            current = "my_profile"
        else:
            current = "leaderboard"
        return TemplateResponse(
            request,
            "leaderboard_personal.html",
            {
                "profile": profile,
                "current": current,
                "matches": matches,
                "names": names,
                "ratings": ratings,
                "labels": labels,
            },
        )

    def _get_match_line_data(self, user: User) -> Tuple[List[int], List[str]]:
        ratings = [1000]
        labels = [user.date_joined.strftime("%d/%m/%Y")]
        for score in MatchResult.get_player_scores(user).order_by("date"):
            ratings.append(ratings[-1] + score.rate_change)
            labels.append(score.date.strftime("%d/%m/%Y"))
        return ratings, labels


class LeaderboardCompareView(BaseView):
    def get(self, request, name: str, other_name: str):
        user = User.objects.get(username=name)
        other_user = User.objects.get(username=other_name)
        matches = sorted(
            get_player_rating_data(MatchResult.get_player_scores(user, other_user)[:50]),
            key=lambda x: x["date"],
            reverse=True,
        )
        profile, other_profile = get_comparative_player_data(user, other_user)
        if user == request.user:
            current = "my_profile"
        else:
            current = "leaderboard"
        return TemplateResponse(
            request,
            "leaderboard_compare.html",
            {"profile": profile, "other_profile": other_profile, "current": current, "matches": matches},
        )


class LeaderboardDeleteView(BaseView):
    def get(self, request, db_id: str):
        match = MatchResult.objects.get(id=db_id)
        if TournamentGame.objects.filter(match_id=match.match_id).first() is not None:
            # no
            return HttpResponseRedirect(f"/leaderboard/{request.user.username}")
        player = UserData.objects.get(user=match.player)
        opponent = UserData.objects.get(user=match.opponent)
        result = match.get_result()
        if result == Result.WIN:
            player.wins -= 1
            opponent.losses -= 1
        elif result == Result.LOSS:
            player.losses -= 1
            opponent.wins -= 1
        else:
            player.ties -= 1
            opponent.ties -= 1
        player.rating -= match.rate_change
        opponent.rating += match.rate_change
        player.save()
        opponent.save()
        MatchResult.objects.filter(match_id=match.match_id).delete()
        return HttpResponseRedirect(f"/leaderboard/{request.user.username}")
