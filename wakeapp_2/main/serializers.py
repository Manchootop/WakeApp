from django.contrib.auth import get_user_model
from rest_framework import serializers

from wakeapp_2.main.models import Event, EventVisibility

UserModel = get_user_model()


class EventSerializer(serializers.ModelSerializer):
    visible_to_friends = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        model = Event
        fields = ('name', 'creator', 'created_at', 'visible_to', 'location', 'date', 'visible_to_friends')
        read_only_fields = ('creator', 'created_at')

    def create(self, validated_data):
        visible_to_friends = validated_data.pop('visible_to_friends')
        event = Event.objects.create(**validated_data)
        for friend_id in visible_to_friends:
            event_visibility = EventVisibility.objects.create(event=event, user_id=friend_id)
        return event


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'username', 'first_name', 'last_name')
