import math
from typing import Tuple

from login.models import UserData
from scoreboard.models import MatchResult, Result
from scoreboard.src import constants


def record_score(player: UserData, opponent: UserData, match: MatchResult):
    """
    A single score record of the 2 calculates the change in score for both the player and opponent
    """
    outcome = 0.5
    result = match.get_result()
    if result == Result.WIN:
        outcome = 1
        player.wins += 1
        opponent.losses += 1
    elif result == Result.LOSS:
        opponent.wins += 1
        player.losses += 1
        outcome = 0
    else:
        player.ties += 1
        opponent.ties += 1
    rate_change_player, rate_change_opponent = _elo_rating(player.rating, opponent.rating, outcome)
    player.rating += rate_change_player
    opponent.rating += rate_change_opponent
    player.save()
    opponent.save()
    match.rate_change = rate_change_player
    match.save()


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
