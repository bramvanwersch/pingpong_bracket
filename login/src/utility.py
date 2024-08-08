from typing import List, Dict, Iterable

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
        if Scores.objects.filter(player1=player.user).first() is None and Scores.objects.filter(player2=player.user).first() is None:
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
