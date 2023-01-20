from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from wakeapp_2.friendship.managers import FriendshipManager

UserModel = get_user_model()


class Friend(models.Model):
    to_user = models.ForeignKey(
        UserModel,
        models.CASCADE,
        related_name='friends'
    )

    from_user = models.ForeignKey(
        UserModel,
        models.CASCADE,
        related_name="unaccepted_friend_relation"
    )
    created = models.DateTimeField(default=timezone.now)

    objects = FriendshipManager()

    class Meta:
        unique_together = ('from_user', "to_user")

    def __str__(self):
        return f'User {self.from_user_id} friendship requested {self.to_user_id}'


# class FriendshipRequest(models.Model):
#     from_user = models.ForeignKey(
#         UserModel,
#         on_delete=models.CASCADE,
#         related_name="friendship_requests_sent",
#     )
#     to_user = models.ForeignKey(
#         UserModel,
#         on_delete=models.CASCADE,
#         related_name="friendship_requests_received"
#     )
#
#     message = models.TextField(blank=True)
#
#     created = models.DateTimeField(default=timezone.now)
#     rejected = models.DateTimeField(blank=True, null=True)
#     viewed = models.DateTimeField(blank=True, null=True)
#
#     class Meta:
#         unique_together = ('from_user', 'to_user')
#
#     def __str__(self):
#         return f'User {self.from_user_id} friendship requested {self.to_user_id}'
#
#     def accept(self):
#         # assign friendship for sender
#         Friend.objects.create(from_user=self.from_user, to_user=self.to_user)
#         # assign friendship for receiver
#         Friend.objects.create(from_user=self.to_user, to_user=self.from_user)
#
#         # TODO signal
#
#         # delete record from this model as its role is to handle requests
#         # Friend model is to contain and friends, so we record accepted requests there
#         self.delete()
#
#         # delete reverse friend request
#         FriendshipRequest.objects.filter(
#             from_user=self.to_user, to_user=self.from_user
#         ).delete()
#
#         return True
#
#     def reject(self):
#         self.rejected = timezone.now()
#         self.save()
#         return True
#
#     def cancel(self):
#         self.delete()
#         return True
#
#     def mark_viewed(self):
#         self.viewed = timezone.now()
#         self.save()
#         return True
