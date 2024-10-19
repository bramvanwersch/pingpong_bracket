import math

from django.http import HttpResponse
from rest_framework.views import APIView

from login.models import UserData
from scoreboard.models import MatchResult, Result
from scoreboard.src.score import record_match_results
from tournaments.models import Tournament, TournamentGame


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
        game = TournamentGame.objects.get(pk=db_id)
        if game.game_type == str(TournamentGame.GameType.ELIMINATION):
            if score1 == score2:
                return HttpResponse("Ties are not allowed in elimination games", status=400)
        p1_data = UserData.objects.get(user=game.player1)
        p2_data = UserData.objects.get(user=game.player2)
        m1, _ = record_match_results(p1_data, p2_data, score1, score2)
        game.match_id = m1.match_id
        if game.game_type == str(TournamentGame.GameType.ELIMINATION):
            self._next_elimination_game(game)
        game.save()
        return HttpResponse()

    def _next_elimination_game(self, game: TournamentGame):
        p1_match = MatchResult.objects.get(player=game.player1, match_id=game.match_id)
        proceeding_player = game.player1
        if p1_match.get_result() != Result.WIN:
            proceeding_player = game.player2

        next_game = TournamentGame.objects.filter(
            round=game.round + 1, round_number=math.ceil(game.round_number / 2), tournament_id=game.tournament_id
        ).first()
        if next_game is None:
            # should mean this was the final round
            tournament = game.tournament
            tournament.status = Tournament.TournamentState.FINISHED
            tournament.save()
            return
        if game.round_number / 2 % 1 != 0 and next_game.player1 is None:
            next_game.player1 = proceeding_player
        else:
            next_game.player2 = proceeding_player
        next_game.save()
