from typing import Dict, Iterable, List

from scoreboard.models import MatchResult, Result
from tournaments.models import TournamentGame


def get_rating_data(matches: Iterable[MatchResult], max_: int = 25) -> List[Dict[str, str]]:
    data = []
    matches = list(matches)
    tournament_map = {
        g.match_id: g.tournament
        for g in TournamentGame.objects.filter(match_id__in=[m.match_id for m in matches]).select_related("tournament")
    }
    covered = set()
    for match in matches:
        if match.match_id in covered:
            continue
        tournament = tournament_map.get(match.match_id, None)
        covered.add(match.match_id)
        result = match.get_result()
        if result == Result.WIN:
            result = f"{match.player.username} Won"
        elif result == Result.LOSS:
            result = f"{match.opponent.username} Won"
        rating = abs(round(match.rate_change, 2))
        data.append(
            {
                "player1": match.player.username,
                "player2": match.opponent.username,
                "result": result,
                "score": f"{match.player_score} : {match.opponents_score}",
                "rating": rating,
                "date": match.date.date().isoformat(),
                "db_id": match.id,
                "tournament_name": tournament.name if tournament else tournament,
                "tournament_id": tournament.pk if tournament else tournament,
            }
        )
        if len(data) >= max_:
            break
    return data


def get_player_rating_data(matches: Iterable[MatchResult]) -> List[Dict[str, str]]:
    data = []
    # collect the iterable in case
    matches = list(matches)
    tournament_map = {
        g.match_id: g.tournament
        for g in TournamentGame.objects.filter(match_id__in=[m.match_id for m in matches]).select_related("tournament")
    }
    for match in matches:
        result = match.get_result()
        tournament = tournament_map.get(match.match_id, None)
        data.append(
            {
                "player1": match.player.username,
                "player2": match.opponent.username,
                "result": result,
                "score": f"{match.player_score} : {match.opponents_score}",
                "rating": round(match.rate_change, 2),
                "date": match.date.date().isoformat(),
                "db_id": match.id,
                "tournament_name": tournament.name if tournament else tournament,
                "tournament_id": tournament.pk if tournament else tournament,
            }
        )
    return data
