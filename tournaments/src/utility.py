from typing import Iterable

from tournaments.models import Tournament, TournamentParticipant


def tournament_table_data(tournaments: Iterable[Tournament]):
    final_data = []
    for tournament in tournaments:
        participants = list(TournamentParticipant.objects.filter(tournament=tournament).select_related("user"))
        final_data.append({
            "name": tournament.name,
            "start_date": tournament.start_date,
            "end_date": tournament.end_date,
            "status": tournament.status,
            "nr_participants": len(participants),
            "tournament_type": tournament.tournament_type,
            "invite_only": tournament.invite_only,
            "creator": tournament.creator,
            "db_id": tournament.pk,
            "participants": [p.user for p in participants]
        })
    return final_data
