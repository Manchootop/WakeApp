from django.db import models

from wakeapp_2.friendship.models import Friend


class FriendshipManager(models.Manager):
    def friends(self, user):
        qs = Friend.objects.select_related("from_user").filter(to_user=user)
        friends = [u.from_user for u in qs]


        return friends
