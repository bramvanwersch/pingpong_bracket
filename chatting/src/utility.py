from typing import Dict, List, Union

from django.db.models.functions import Lower

from chatting.models import ChatGroupUser
from login.models import User


def get_user_mapping(exclude_users: List["User"] = None) -> Dict[str, int]:
    names = {u.username: u.pk for u in User.objects.all().order_by(Lower("username"))}
    if exclude_users is None:
        exclude_users = []
    for user in exclude_users:
        del names[user.username]
    return names


def get_group_mapping(requesting_user: User) -> List[List[Union[str, int]]]:
    user_groups = ChatGroupUser.objects.filter(user=requesting_user).select_related("group")
    group_names = [[ug.group.name, f"{ug.group.pk}"] for ug in user_groups]
    return group_names
