import os

from django.db import transaction
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from rest_framework.views import APIView

from general_src import image_handling
from tournaments.models import TournamentGame, TournamentPrize


@method_decorator(transaction.non_atomic_requests, name="dispatch")
class SetGameScore(APIView):
    def post(self, request, db_id):
        score1 = request.data.get("p1_score", 0)
        score2 = request.data.get("p2_score", 0)
        try:
            score1 = int(score1)
            score2 = int(score2)
        except ValueError:
            return HttpResponse("Non numeric score(s) provided", status=400)
        if score1 < 0 or score2 < 0:
            return HttpResponse("Scores must be above 0", status=400)
        if score1 == score2 == 0:
            return HttpResponse("Please fill in scores above 0", status=400)
        game = TournamentGame.objects.filter(pk=db_id).select_related("tournament").first()

        format_ = game.tournament.get_tournament_format()
        try:
            format_.score_game(game, score1, score2)
        except RuntimeError as e:
            return HttpResponse(str(e), status=400)
        return HttpResponse()


class SetTrophy(APIView):
    def post(self, request, tournament_id: str, place: str):
        file = request.FILES["file"]
        try:
            image_handling.verify_image(file)
        except RuntimeError as e:
            return HttpResponse(str(e), status=400)
        prize = TournamentPrize.objects.get(tournament_id=tournament_id, place=int(place))
        if prize.trophy.name != "default_prize.png":
            try:
                os.remove(prize.trophy.path)
            except FileNotFoundError:
                pass
        prize.trophy = file
        prize.save()
        return HttpResponse()
