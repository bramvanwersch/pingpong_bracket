from django.shortcuts import redirect
from django.template.response import TemplateResponse

from chatting.src import utility as chatting_utility
from general_src.base_view import BaseView
from tournaments.models import Tournament, TournamentParticipant
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


class TournamentDetailView(BaseView):
    def get(self, request, tournament_id):
        tournament = Tournament.objects.get(pk=tournament_id)
        data = utility.tournament_table_data([tournament])[0]
        return TemplateResponse(request, "tournaments_detail.html", {"data": data})
