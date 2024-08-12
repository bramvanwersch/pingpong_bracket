import datetime

from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from general_src.base_view import BaseView
from matchmaking.models import MatchRequests
from matchmaking.src.utility import get_match_request_data


class MatchmakingView(BaseView):

    def get(self, request):
        current = datetime.datetime.now()
        waiting_matches = MatchRequests.objects.filter(start__lt=current).filter(end__gt=current).filter(challenger=None)
        request_data = get_match_request_data(waiting_matches)
        planned_matches = MatchRequests.objects.filter(start__lt=current).filter(end__gt=current).exclude(challenger=None).filter(Q(challenger=request.user) | Q(asker=request.user))
        planned_data = get_match_request_data(planned_matches)
        return TemplateResponse(request, "matchmaking.html", {"current": "matchmaking", "requests": request_data, "planned": planned_data, "active_matches": planned_data})


class AddMatchRequest(BaseView):

    def post(self, request):
        data = request.POST
        MatchRequests.objects.create(start=data["from"], end=data["to"], asker=request.user, match_type=MatchRequests.MatchTypes.REQUEST)
        return HttpResponseRedirect("/matchmaking/")


class DeleteMatchRequest(BaseView):

    def get(self, request, db_id: str):
        MatchRequests.objects.get(id=db_id).delete()
        return HttpResponseRedirect("/matchmaking/")


class AcceptRequest(BaseView):

    def get(self, request, db_id: str):
        match_request = MatchRequests.objects.get(id=db_id)
        match_request.challenger = request.user
        match_request.save()
        return HttpResponseRedirect("/matchmaking/")


class RetractRequest(BaseView):

    def get(self, request, db_id: str):
        match_request = MatchRequests.objects.get(id=db_id)
        if match_request.match_type == MatchRequests.MatchTypes.CHALLENGE:
            match_request.delete()
        elif request.user.username == match_request.asker.username:
            match_request.delete()
        else:
            match_request.challenger = None
            match_request.save()
        return HttpResponseRedirect("/matchmaking/")


class ChallengeRequest(BaseView):

    def get(self, request, name: str):
        asker = User.objects.get(username=name)
        start = datetime.datetime.now()
        end = start + datetime.timedelta(hours=2)
        MatchRequests.objects.create(asker=asker, challenger=request.user, start=start, end=end, match_type=MatchRequests.MatchTypes.CHALLENGE)
        return HttpResponseRedirect("/matchmaking/")
