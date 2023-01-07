from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()

from django.db import models
from django.contrib.auth import get_user_model


class Event(models.Model):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    visible_to = models.ManyToManyField(UserModel, through='EventVisibility', related_name='visible_events')
    location = models.CharField(max_length=255, blank=True)
    date = models.DateTimeField()


class EventVisibility(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
