import datetime
import random
from collections import defaultdict
from typing import List

from django.shortcuts import redirect
from django.template.response import TemplateResponse

from chatting.src import utility as chatting_utility
from general_src.base_view import BaseView
from scoreboard.models import MatchResult
from tournaments.models import Tournament, TournamentGame, TournamentParticipant
from tournaments.src import utility


class TournamentMainView(BaseView):
    def get(self, request):
        names = chatting_utility.get_user_mapping([request.user])
        types = [c[0] for c in Tournament.TournamentType.choices]
        tournament_objects = Tournament.objects.all().order_by("start_date")[:50]
        tournament_data = utility.tournament_table_data(tournament_objects)
        issue = ""
        if "issue" in request.session:
            issue = request.session.pop("issue")
        return TemplateResponse(
            request,
            "tournaments_overview.html",
            {"names": names, "issue": issue, "types": types, "tournament_data": tournament_data},
        )


class CreateTournamentView(BaseView):
    def post(self, request):
        data = request.POST
        name = data.get("name", None)
        if not name:
            request.session["issue"] = "Please provide a name"
            return redirect("/tournament/")
        only_direct = data.get("only_direct", None) == "on"
        invitees = data.getlist("invitees", [])
        type_ = data.get("tournamnet_type")
        if only_direct and len(invitees) <= 1:
            request.session["issue"] = "When using direct invites, invite at least 2 people"
            return redirect("/tournament/")
        tournament = Tournament.objects.create(
            creator=request.user,
            name=name,
            status=Tournament.TournamentState.NOT_STARTED,
            tournament_type=type_,
            invite_only=only_direct,
        )
        TournamentParticipant.objects.create(user_id=request.user.pk, tournament=tournament)
        for invite in invitees:
            TournamentParticipant.objects.create(user_id=invite, tournament=tournament)
        return redirect("/tournament/")


class StartTournamentView(BaseView):
    def post(self, request, tournament_id: str):
        data = request.POST
        try:
            end_date = datetime.date.fromisoformat(data.get("end_date", None))
        except ValueError:
            request.session["issue"] = "Invalid end date information"
            return redirect(f"/tournament/detail/{tournament_id}")
        start_date = datetime.date.today()
        if end_date <= start_date:
            request.session["issue"] = "End date must be larger then start date"
            return redirect(f"/tournament/detail/{tournament_id}")
        tournament = Tournament.objects.get(pk=tournament_id)
        participants = [
            tp.user for tp in TournamentParticipant.objects.filter(tournament=tournament).select_related("user")
        ]
        random.shuffle(participants)
        if len(participants) < 2:
            request.session["issue"] = "A tournament must have at least 2 participants"
            return redirect(f"/tournament/detail/{tournament_id}")
        tournament.start_date = start_date
        tournament.end_date = end_date
        if tournament.tournament_type == "Single elimination":
            self._create_elimination_games(participants, tournament, start_date, end_date)
        tournament.status = "Running"
        tournament.save()
        return redirect(f"/tournament/detail/{tournament_id}")

    def _create_elimination_games(
        self,
        participants: List[TournamentParticipant],
        tournament: Tournament,
        start_date: datetime.date,
        end_date: datetime.date,
    ):
        total_days = (end_date - start_date).days
        nr_rounds = 1
        while 2**nr_rounds < len(participants):
            nr_rounds += 1
        days_per_round = int(total_days / nr_rounds)
        round_data = {}
        for power, round_nr in enumerate(range(nr_rounds, 0, -1)):
            nr_games = 2**power
            round_end_date = end_date - datetime.timedelta(days=(round_nr - 1) * days_per_round)
            round_data[round_nr] = []
            for game_nr in range(1, nr_games + 1):
                game = TournamentGame.objects.create(
                    round_number=game_nr,
                    round=round_nr,
                    game_type="Elimination",
                    tournament=tournament,
                    end_date=round_end_date,
                )
                round_data[round_nr].append(game)
        missing = 2**nr_rounds - len(participants)
        current_participant = 0
        while current_participant < missing:
            game = round_data[2][missing - current_participant - 1]
            game.player1 = participants[current_participant]
            current_participant += 1
            if current_participant >= missing:
                game.save()
                break
            game.player2 = participants[current_participant]
            current_participant += 1
            game.save()
        count = 0
        while current_participant < len(participants):
            game = round_data[1][count]
            game.player1 = participants[current_participant]
            current_participant += 1
            game.player2 = participants[current_participant]
            current_participant += 1
            game.save()
            count += 1
        for game in round_data[1]:
            if game.player1 is None and game.player2 is None:
                game.is_dummy = True
                game.save()


class TournamentDetailView(BaseView):
    def get(self, request, tournament_id):
        tournament = Tournament.objects.get(pk=tournament_id)
        data = utility.tournament_table_data([tournament])[0]
        games = list(TournamentGame.objects.filter(tournament=tournament_id).select_related("player1", "player2"))
        matches = MatchResult.objects.filter(match_id__in=[g.match_id for g in games])
        matches_map = defaultdict(list)
        for match in matches:
            matches_map[match.match_id].append(match)
        game_data = []
        for game in games:
            m1, m2 = matches_map.get(game.match_id, [None, None])
            if m1 or m2 is None:
                p1_score = 0
                p2_score = 0
            else:
                if m1.player_id == game.player1.pk:
                    p1_score = m1.player_score
                    p2_score = m2.player_score
                else:
                    p1_score = m2.player_score
                    p2_score = m1.player_score
            game_data.append(
                {
                    "player1": game.player1,
                    "player2": game.player2,
                    "p1_score": p1_score,
                    "p2_score": p2_score,
                    "dummy": game.is_dummy,
                }
            )
        issue = ""
        if "issue" in request.session:
            issue = request.session.pop("issue")
        return TemplateResponse(
            request, "tournaments_detail.html", {"data": data, "issue": issue, "elimination_games": game_data}
        )


class LeaveTournamentView(BaseView):
    def get(self, request, tournament_id):
        TournamentParticipant.objects.filter(tournament_id=tournament_id, user=request.user).delete()
        return redirect(f"/tournament/detail/{tournament_id}")


class JoinTournamentView(BaseView):
    def get(self, request, tournament_id):
        TournamentParticipant.objects.create(tournament_id=tournament_id, user=request.user)
        return redirect(f"/tournament/detail/{tournament_id}")


class DeleteTournamentView(BaseView):
    def get(self, request, tournament_id):
        tournament = Tournament.objects.get(pk=tournament_id)
        TournamentParticipant.objects.filter(tournament_id=tournament_id).delete()
        tournament.delete()
        return redirect("/tournament/")
