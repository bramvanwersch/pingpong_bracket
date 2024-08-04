import math
from typing import Tuple

from login.models import UserData
from scoreboard.models import Scores
from scoreboard.src import constants


def record_score(p1_data: UserData, p2_data: UserData, score: Scores):
    outcome = 0.5
    p1_score = score.p1_score
    p2_score = score.p2_score
    if p1_score > p2_score:
        outcome = 1
        p1_data.wins += 1
        p2_data.losses += 1
    elif p2_score > p1_score:
        p2_data.wins += 1
        p1_data.losses += 1
        outcome = 0
    else:
        p1_data.ties += 1
        p2_data.ties += 1
    new_rate1, new_rate2 = _elo_rating(p1_data.rating, p2_data.rating, outcome)
    p1_data.rating += new_rate1
    p2_data.rating += new_rate2
    p1_data.save()
    p2_data.save()
    score.p1_rate_change = new_rate1
    score.p2_rate_change = new_rate2
    score.save()


def _elo_rating(rating_a: float, rating_b: float, outcome: float) -> Tuple[float, float]:
    # https://www.geeksforgeeks.org/elo-rating-algorithm/
    # Calculate the Winning Probability of Player B
    probabilty_b = _probability(rating_a, rating_b)

    # Calculate the Winning Probability of Player A
    probabilty_a = _probability(rating_b, rating_a)

    rating_a = constants.K * (outcome - probabilty_a)
    rating_b = constants.K * ((1 - outcome) - probabilty_b)
    return rating_a, rating_b


def _probability(rating1, rating2) -> float:
    # Calculate and return the expected score
    return 1.0 / (1 + math.pow(10, (rating1 - rating2) / 400.0))
