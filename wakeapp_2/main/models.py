from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()

from django.db import models
from django.contrib.auth import get_user_model


class Event(models.Model):
    # Fields for the event content
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Field for the user who created the event
    creator = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    # Field for the list of friends who are allowed to view the event
    friends = models.ManyToManyField(UserModel, related_name='viewable_events')

    def __str__(self):
        return self.title
