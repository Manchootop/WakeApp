from django.contrib.auth import get_user_model
from django.shortcuts import render

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from .models import Friendship
from .serializers import FriendshipSerializer

UserModel = get_user_model()


class FriendshipViewSet(viewsets.ModelViewSet):
    serializer_class = FriendshipSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        # Get the list of friendships where the user is the sender or receiver
        friendships = Friendship.objects.filter(Q(sender=self.request.user) | Q(receiver=self.request.user))

        # Filter the friendships to only include accepted ones
        return friendships.filter(status='accepted')


class SendFriendshipRequestView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request):
        # Get the user that the request is being sent to
        receiver = UserModel.objects.get(id=request.data['receiver'])

        # Create a new friendship with a status of 'pending'
        friendship = Friendship.objects.create(
            sender=request.user,
            receiver=receiver,
            status='pending'
        )

        serializer = FriendshipSerializer(friendship)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AcceptFriendshipRequestView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def update(self, request, pk=None):
        # Get the friendship request
        friendship = Friendship.objects.get(id=pk)

        # Ensure that the request is being accepted by the intended receiver
        if friendship.receiver != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        # Update the status of the request to 'accepted'
        friendship.status = 'accepted'
        friendship.save()

        serializer = FriendshipSerializer(friendship)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RejectFriendshipRequestView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def update(self, request, pk=None):
        # Get the friendship request
        friendship = Friendship.objects.get(id=pk)

        # Ensure that the request is being rejected by the intended receiver
        if friendship.receiver != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        # Update the status of the request to 'rejected'
        friendship.status = 'rejected'
        friendship.save()

        serializer = FriendshipSerializer(friendship)
        return Response(serializer.data, status=status.HTTP_200_OK)

    '''
    
    PUT /api/friendships/123/
    { "status": "rejected" }
    
'''
