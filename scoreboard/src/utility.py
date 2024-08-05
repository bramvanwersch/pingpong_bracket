from typing import List, Dict, Iterable

from django.contrib.auth.models import User

from scoreboard.models import Scores


def get_rating_data(scores: Iterable[Scores]) -> List[Dict[str, str]]:
    data = []
    for score in scores:
        result = "Tie"
        if score.p1_score > score.p2_score:
            result = f"{score.player1.username} Won"
        elif score.p2_score > score.p1_score:
            result = f"{score.player2.username} Won"
        rating = abs(round(score.p1_rate_change, 2))
        data.append({
            "player1": score.player1.username,
            "player2": score.player2.username,
            "result": result,
            "score": f"{score.p1_score} : {score.p2_score}",
            "rating": rating,
            "date": score.date.date().isoformat(),
            "db_id": score.id
        })
    return data


def get_player_rating_data(scores: Iterable[Scores], player: User) -> List[Dict[str, str]]:
    data = []
    for score in scores:
        result = "Tie"
        if score.p1_score > score.p2_score:
            if score.player1 == player:
                result = f"Win"
            else:
                result = "Loss"
        elif score.p2_score > score.p1_score:
            if score.player1 == player:
                result = f"Loss"
            else:
                result = "Win"
        if score.player1 == player:
            rating = round(score.p1_rate_change, 2)
        else:
            rating = -1 * round(score.p1_rate_change, 2)
        data.append({
            "player1": score.player1.username,
            "player2": score.player2.username,
            "result": result,
            "score": f"{score.p1_score} : {score.p2_score}",
            "rating": rating,
            "date": score.date.date().isoformat(),
            "db_id": score.id
        })
    return data
