from typing import Dict, Iterable, List, Tuple, Union

from django.contrib.auth.models import User

from login.models import UserData
from scoreboard.models import MatchResult, Result


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
        if MatchResult.get_player_scores(player.user).first() is None:
            rating = "NA"
        data.append(
            {
                "name": player.user.username,
                "rating": rating,
                "wins": player.wins,
                "losses": player.losses,
                "ties": player.ties,
                "winrate": winrate,
                "total_games": player.total,
                "image_url": player.profile_picture.url,
            }
        )
    return data


def get_comparative_player_data(
    player1: User, player2: User
) -> Tuple[Dict[str, Union[int, float]], Dict[str, Union[int, float]]]:
    matches = MatchResult.get_player_scores(player1, player2)
    p1_data = {
        "name": player1.username,
        "rating_gain": 0,
        "wins": 0,
        "losses": 0,
        "ties": 0,
        "total": len(matches),
        "winrate": 0,
    }
    p2_data = {key: value for key, value in p1_data.items()}
    p2_data["name"] = player2.username
    for match in matches:
        result = match.get_result()
        if result == Result.WIN:
            p1_data["wins"] += 1
            p2_data["losses"] += 1
        elif result == Result.LOSS:
            p1_data["losses"] += 1
            p2_data["wins"] += 1
        else:
            p1_data["ties"] += 1
            p2_data["ties"] += 1
        p1_data["rating_gain"] += match.rate_change
        p2_data["rating_gain"] -= match.rate_change
    try:
        p1_data["winrate"] = round(p1_data["wins"] / p1_data["total"], 2) * 100
    except ZeroDivisionError:
        p1_data["winrate"] = "NA"
    try:
        p2_data["winrate"] = round(p2_data["wins"] / p2_data["total"], 2) * 100
    except ZeroDivisionError:
        p2_data["winrate"] = "NA"
    p1_data["rating_gain"] = round(p1_data["rating_gain"], 2)
    p2_data["rating_gain"] = round(p2_data["rating_gain"], 2)
    return p1_data, p2_data
