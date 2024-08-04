from typing import List, Dict, Iterable

from login.models import UserData


def get_player_data(players: Iterable[UserData]) -> List[Dict[str, str]]:
    data = []
    for player in players:
        try:
            winrate = round(player.wins / player.losses, 2)
        except ZeroDivisionError:
            winrate = "NA"
        data.append({
            "name": player.user.username,
            "rating": round(player.rating, 2),
            "wins": player.wins,
            "losses": player.losses,
            "ties": player.ties,
            "winrate": winrate,
            "total_games": player.wins + player.losses + player.ties
        })
    return data
