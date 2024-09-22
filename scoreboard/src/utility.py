from typing import List, Dict, Iterable

from scoreboard.models import MatchResult, Result


def get_rating_data(matches: Iterable[MatchResult], max_: int = 25) -> List[Dict[str, str]]:
    data = []
    covered = set()
    for match in matches:
        if match.match_id in covered:
            continue
        covered.add(match.match_id)
        result = match.get_result()
        if result == Result.WIN:
            result = f"{match.player.username} Won"
        elif result == Result.LOSS:
            result = f"{match.opponent.username} Won"
        rating = abs(round(match.rate_change, 2))
        data.append({
            "player1": match.player.username,
            "player2": match.opponent.username,
            "result": result,
            "score": f"{match.player_score} : {match.opponents_score}",
            "rating": rating,
            "date": match.date.date().isoformat(),
            "db_id": match.id
        })
        if len(data) >= max_:
            break
    return data


def get_player_rating_data(matches: Iterable[MatchResult]) -> List[Dict[str, str]]:
    data = []
    for match in matches:
        result = match.get_result()
        data.append({
            "player1": match.player.username,
            "player2": match.opponent.username,
            "result": result,
            "score": f"{match.player_score} : {match.opponents_score}",
            "rating": round(match.rate_change, 2),
            "date": match.date.date().isoformat(),
            "db_id": match.id
        })
    return data
