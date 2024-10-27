from collections import defaultdict
from typing import Any, Dict, Iterable, List

from scoreboard.models import MatchResult, Result
from tournaments.models import Tournament, TournamentGame, TournamentParticipant, TournamentPrize


def tournament_table_data(tournaments: Iterable[Tournament], add_places: bool = False):
    final_data = []
    for tournament in tournaments:
        participants = list(
            TournamentParticipant.objects.filter(tournament=tournament).select_related("user").order_by("place")
        )
        places = {}
        if add_places:
            places = [
                {"place": nr + 1, "prize": None, "player": "-"}
                for nr in range(TournamentParticipant.objects.filter(tournament=tournament).count())
            ]
            prizes = TournamentPrize.objects.filter(tournament=tournament)
            for participant in participants:
                if participant.place is None:
                    continue
                place = places[participant.place - 1]
                place["player"] = participant.user.username
            for prize in prizes:
                try:
                    places[prize.place - 1]["prize"] = prize.trophy.url
                except IndexError:
                    continue
        final_data.append(
            {
                "name": tournament.name,
                "start_date": tournament.start_date,
                "end_date": tournament.end_date,
                "status": tournament.status,
                "nr_participants": len(participants),
                "tournament_type": tournament.tournament_type,
                "invite_only": tournament.invite_only,
                "creator": tournament.creator,
                "db_id": tournament.pk,
                "participants": [p.user for p in participants],
                "places": places,
            }
        )
    return final_data


def get_tournament_match_details(games: Iterable[TournamentGame]) -> List[Dict[str, Any]]:
    matches = MatchResult.objects.filter(match_id__in=[g.match_id for g in games])
    matches_map = defaultdict(list)
    for match in matches:
        matches_map[match.match_id].append(match)
    game_data = []
    for game in games:
        m1, m2 = matches_map.get(game.match_id, [None, None])
        result = "tbd"
        if m1 is None or m2 is None:
            p1_score = 0
            p2_score = 0
        else:
            if m1.player_id == game.player1.pk:
                p1_score = m1.player_score
                p2_score = m2.player_score
                if m1.get_result() == str(Result.WIN):
                    result = f"{game.player1.username} Won"
                else:
                    result = f"{game.player2.username} Won"
            else:
                p1_score = m2.player_score
                p2_score = m1.player_score
                if m2.get_result() == str(Result.WIN):
                    result = f"{game.player2.username} Won"
                else:
                    result = f"{game.player1.username} Won"
        game_data.append(
            {
                "player1": game.player1.username if game.player1 is not None else "tbd",
                "player2": game.player2.username if game.player2 is not None else "tbd",
                "p1_score": p1_score,
                "p2_score": p2_score,
                "round_number": game.round_number,
                "round": game.round,
                "db_id": game.pk,
                "end_date": game.end_date.strftime("%d-%b"),
                "dummy": str(game.is_dummy).lower(),
                "result": result,
            }
        )
    return game_data
