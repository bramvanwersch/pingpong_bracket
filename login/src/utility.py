from typing import List, Dict, Iterable, Tuple, Union

from django.contrib.auth.models import User

from login.models import UserData
from scoreboard.models import Scores


def get_player_data(players: Iterable[UserData]) -> List[Dict[str, str]]:
    data = []
    for player in players:
        try:
            winrate = round(player.wins / player.total, 2) * 100
        except ZeroDivisionError:
            if player.wins == 0:
                winrate = "NA"
            else:
                winrate = 1.0
        rating = round(player.rating, 2)
        if Scores.get_player_scores(player.user).first() is None:
            rating = "NA"
        data.append({
            "name": player.user.username,
            "rating": rating,
            "wins": player.wins,
            "losses": player.losses,
            "ties": player.ties,
            "winrate": winrate,
            "total_games": player.total
        })
    return data


def get_comparative_player_data(player1: User, player2: User) -> Tuple[Dict[str, Union[int, float]], Dict[str, Union[int, float]]]:
    scores = Scores.get_player_scores(player1, player2)
    p1_data = {
        "name": player1.username,
        "rating_gain": 0,
        "wins": 0,
        "losses": 0,
        "ties": 0,
        "total": 0,
        "winrate": 0
    }
    p2_data = {key: value for key, value in p1_data.items()}
    p2_data["name"] = player2.username
    for score in scores:
        if score.p1_score > score.p2_score:
            p1_data["wins"] += 1
            p2_data["losses"] += 1
        elif score.p2_score > score.p1_score:
            p1_data["losses"] += 1
            p2_data["wins"] += 1
        else:
            p2_data["ties"] += 1
            p1_data["ties"] += 1
        p1_data["total"] += 1
        p2_data["total"] += 1
        p1_data["rating_gain"] += score.p1_rate_change
        p2_data["rating_gain"] += score.p2_rate_change
    p1_data["winrate"] = round(p1_data["wins"] / p1_data["total"], 2)
    p2_data["winrate"] = round(p2_data["wins"] / p2_data["total"], 2)
    return p1_data, p2_data
