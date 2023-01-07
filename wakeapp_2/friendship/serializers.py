from abc import ABC

from rest_framework import serializers

from wakeapp_2.friendship.models import Friendship


class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = ['id', 'sender', 'receiver', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class FriendshipRequestSerializer(serializers.Serializer, ABC):
    receiver = serializers.IntegerField()


class FriendshipResponseSerializer(serializers.Serializer, ABC):
    status = serializers.ChoiceField(choices=Friendship.STATUS_CHOICES)
