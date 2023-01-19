from abc import ABC

from rest_framework import serializers

from wakeapp_2.friendship.models import FriendshipRequest


class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendshipRequest
        fields = ['id', 'sender', 'receiver', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class FriendshipRequestSerializer(serializers.Serializer, ABC):
    receiver = serializers.IntegerField()


class FriendshipResponseSerializer(serializers.Serializer, ABC):
    status = serializers.ChoiceField(choices=FriendshipRequest.STATUS_CHOICES)
