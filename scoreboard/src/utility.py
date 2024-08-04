from typing import List, Dict, Iterable

from scoreboard.models import Scores


def get_rating_data(scores: Iterable[Scores], mode_general: bool = True) -> List[Dict[str, str]]:
    data = []
    for score in scores:
        result = "Tie"
        if score.p1_score > score.p2_score:
            if mode_general:
                result = f"{score.player1.username} Won"
            else:
                result = f"Win"
        elif score.p2_score > score.p1_score:
            if mode_general:
                result = f"{score.player2.username} Won"
            else:
                result = f"Loss"
        rating = round(score.p1_rate_change, 2)
        if mode_general:
            rating = abs(rating)
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
