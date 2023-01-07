from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class Friendship(models.Model):
    sender = models.ForeignKey(UserModel, related_name='sender_friendship_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(UserModel, related_name='receiver_friendship_requests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
