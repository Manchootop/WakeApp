from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from wakeapp_2.friendship.exceptions import AlreadyExistsError, AlreadyFriendsError

UserModel = get_user_model()


class FriendshipManager(models.Manager):
    def friends(self, user):
        qs = Friend.objects.select_related("from_user").filter(to_user=user)
        friends = [u.from_user for u in qs]

        return friends

    def add_friend(self, from_user, to_user, message=None):
        """Create a friendship request"""
        if from_user == to_user:
            raise ValidationError("Users cannot be friends with themselves")

        if self.are_friends(from_user, to_user):
            raise AlreadyFriendsError("Users are already friends")

        if FriendshipRequest.objects.filter(
                from_user=from_user, to_user=to_user
        ).exists():
            raise AlreadyExistsError("You already requested friendship from this user.")

        if FriendshipRequest.objects.filter(
                from_user=to_user, to_user=from_user
        ).exists():
            raise AlreadyExistsError("This user already requested friendship from you.")

        if message is None:
            message = ""

        request, created = FriendshipRequest.objects.get_or_create(
            from_user=from_user, to_user=to_user
        )

        if created is False:
            raise AlreadyExistsError("Friendship already requested")

        if message:
            request.message = message
            request.save()

        return request

    def are_friends(self, user1, user2):
        """Are these two users friends?"""
        # user1 = sender, user2 = receiver
        try:
            friends1 = Friend.objects.get(from_user=user1, to_user=user2)
            friends2 = Friend.objects.get(from_user=user2, to_user=user1)
        except Friend.DoesNotExist:
            return False
        if friends1 and user2 in friends1:
            return True
        elif friends2 and user1 in friends2:
            return True
        else:
            try:
                Friend.objects.get(to_user=user1, from_user=user2)
                return True
            except Friend.DoesNotExist:
                return False

    def requests(self, user):
        """Return a list of friendship requests"""
        # key = cache_key("requests", user.pk)
        # requests = cache.get(key)

        # if requests is None:
        qs = FriendshipRequest.objects.filter(to_user=user)
        qs = self._friendship_request_select_related(qs, "from_user", "to_user")
        requests = list(qs)
        # cache.set(key, requests)

        return requests

    def sent_requests(self, user):
        qs = FriendshipRequest.objects.filter(from_user=user)
        qs = self._friendship_request_select_related(qs, "from_user", "to_user")
        requests = list(qs)
        return requests

    def unread_requests(self, user):
        """Return a list of unread friendship requests"""
        # key = cache_key("unread_requests", user.pk)
        # unread_requests = cache.get(key)

        # if unread_requests is None:
        qs = FriendshipRequest.objects.filter(to_user=user, viewed__isnull=True)
        qs = self._friendship_request_select_related(qs, "from_user", "to_user")
        unread_requests = list(qs)
        # cache.set(key, unread_requests)

        return unread_requests

    def unread_request_count(self, user):
        """Return a count of unread friendship requests"""
        # key = cache_key("unread_request_count", user.pk)
        # count = cache.get(key)

        # if count is None:
        count = FriendshipRequest.objects.filter(
            to_user=user, viewed__isnull=True
        ).count()
        # cache.set(key, count)

        return count

    def read_requests(self, user):
        """Return a list of read friendship requests"""
        # key = cache_key("read_requests", user.pk)
        # read_requests = cache.get(key)

        # if read_requests is None:
        qs = FriendshipRequest.objects.filter(to_user=user, viewed__isnull=False)
        qs = self._friendship_request_select_related(qs, "from_user", "to_user")
        read_requests = list(qs)
        # cache.set(key, read_requests)

        return read_requests

    def rejected_requests(self, user):
        """Return a list of rejected friendship requests"""
        qs = FriendshipRequest.objects.filter(to_user=user, rejected__isnull=False)
        rejected_requests = list(qs)
        return rejected_requests

    def unrejected_requests(self, user):
        """All requests that haven't been rejected"""
        qs = FriendshipRequest.objects.filter(to_user=user, rejected__isnull=True)
        unrejected_requests = list(qs)
        return unrejected_requests

    def unrejected_request_count(self, user):
        """Return a count of unrejected friendship requests"""
        count = FriendshipRequest.objects.filter(to_user=user, rejected__isnull=True).count()
        return count


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

    def save(self, *args, **kwargs):
        # Ensure users can't be friends with themselves
        if self.to_user == self.from_user:
            raise ValidationError("Users cannot be friends with themselves.")
        super().save(*args, **kwargs)


class FriendshipRequest(models.Model):
    from_user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="friendship_requests_sent",
    )
    to_user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="friendship_requests_received"
    )

    message = models.TextField(blank=True, null=True)

    created = models.DateTimeField(default=timezone.now)
    rejected = models.DateTimeField(blank=True, null=True)
    viewed = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f'User {self.from_user_id} friendship requested {self.to_user_id}'

    def accept(self):
        # assign friendship for sender
        Friend.objects.create(from_user=self.from_user, to_user=self.to_user)
        # assign friendship for receiver
        Friend.objects.create(from_user=self.to_user, to_user=self.from_user)

        # TODO signal

        # delete record from this model as its role is to handle requests
        # Friend model is to contain and friends, so we record accepted requests there
        self.delete()

        # delete reverse friend request
        FriendshipRequest.objects.filter(
            from_user=self.to_user, to_user=self.from_user
        ).delete()

        return True

    def reject(self):
        self.rejected = timezone.now()
        self.save()
        return True

    def cancel(self):
        self.delete()
        return True

    def mark_viewed(self):
        self.viewed = timezone.now()
        self.save()
        return True
