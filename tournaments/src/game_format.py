import abc
import math

from login.models import UserData
from scoreboard.models import MatchResult, Result
from scoreboard.src.score import record_match_results
from tournaments.models import Tournament, TournamentGame, TournamentParticipant, TournamentPrize


class BaseFormat(abc.ABC):
    def score_game(self, game: TournamentGame, score1: int, score2: int):
        if not self._is_valid_score(score1, score2):
            raise RuntimeError("Invalid score given for this format")
        p1_data = UserData.objects.get(user=game.player1)
        p2_data = UserData.objects.get(user=game.player2)
        m1, _ = record_match_results(p1_data, p2_data, score1, score2)
        game.match_id = m1.match_id
        game.save()
        self._next_game(game)
        self._set_player_placement(game.tournament)

    def _is_valid_score(self, score1: int, score2: int) -> bool:
        return True

    @abc.abstractmethod
    def _next_game(self, game: TournamentGame):
        pass

    @abc.abstractmethod
    def _set_player_placement(self, tournament: Tournament):
        pass

    def _finish_tournament(self, game: TournamentGame):
        tournament = game.tournament
        tournament.status = Tournament.TournamentState.FINISHED
        tournament.save()
        self._give_prizes(tournament)

    def _give_prizes(self, tournament: Tournament):
        self._set_player_placement(tournament)
        top3 = {tp.place: tp for tp in TournamentParticipant.objects.filter(place__in=[1, 2, 3])}
        prizes = TournamentPrize.objects.filter(tournament=tournament)
        for prize in prizes:
            prize.participant = top3[prize.place]
            prize.save()


class EliminationFormat(BaseFormat):
    def _is_valid_score(self, score1: int, score2: int) -> bool:
        return not score1 == score2

    def _next_game(self, game: TournamentGame):
        p1_match = MatchResult.objects.get(player=game.player1, match_id=game.match_id)
        proceeding_player = game.player1
        if p1_match.get_result() != Result.WIN:
            proceeding_player = game.player2

        next_game = TournamentGame.objects.filter(
            round=game.round + 1, round_number=math.ceil(game.round_number / 2), tournament_id=game.tournament_id
        ).first()
        if next_game is None:
            self._finish_tournament(game)
            return
        if game.round_number / 2 % 1 != 0 and next_game.player1 is None:
            next_game.player1 = proceeding_player
        else:
            next_game.player2 = proceeding_player
        next_game.save()

    def _set_player_placement(self, tournament: Tournament):
        tournament_games = list(TournamentGame.objects.filter(tournament_id=tournament.id, is_dummy=False))
        winning_games = list(
            mr
            for mr in MatchResult.objects.filter(match_id__in=[g.match_id for g in tournament_games]).order_by("date")
            if mr.get_result() == Result.WIN
        )
        # set placement of players
        place = len(tournament_games) + 1
        for result in winning_games:
            participant2 = TournamentParticipant.objects.get(user_id=result.opponent_id, tournament_id=tournament.id)
            participant2.place = place
            participant2.save()
            place -= 1
        # add first place
        if place == 1:
            participant1 = TournamentParticipant.objects.get(
                user_id=winning_games[-1].player, tournament_id=tournament.id
            )
            participant1.place = 1
            participant1.save()
