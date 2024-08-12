from typing import Iterable, List, Dict, Any

from login.models import UserData
from matchmaking.models import MatchRequests


def get_match_request_data(matches: Iterable[MatchRequests]) -> List[Dict[str, Any]]:
    data = []
    for match in matches:
        user_data = UserData.objects.get(user=match.asker)
        if match.challenger is not None:
            challenger_data = UserData.objects.get(user=match.challenger)
        else:
            challenger_data = None
        data.append({
            "start": match.start.isoformat().replace("T", " "),
            "end": match.end.isoformat().replace("T", " "),
            "asker": match.asker.username,
            "asker_email": user_data.email,
            "type": match.match_type,
            "challenger": match.challenger.username if match.challenger is not None else "",
            "challenger_email": challenger_data.email if challenger_data is not None else "",
            "db_id": match.id
        })
    return data
