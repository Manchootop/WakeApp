from django.shortcuts import render, get_object_or_404
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from wakeapp_2.main.models import Event, EventVisibility
from wakeapp_2.main.serializers import EventSerializer, UserSerializer

# class CreateEventView(APIView):
#     def post(self, request):
#         serializer = EventSerializer(data=request.data)
#         if serializer.is_valid():
#             event = serializer.save()
#             if event.visibility == 'FRIENDS':
#                 event.visible_to.set(request.data['visible_to'])
#             elif event.visibility == 'ALL_FRIENDS':
#                 event.visible_to.set(request.user.friends.all())
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)

from rest_framework import generics, status


class CreateEventView(generics.CreateAPIView):
    renderer_classes = [BrowsableAPIRenderer]
    serializer_class = EventSerializer

    def post(self, request, *args, **kwargs):
        # Validate and deserialize the friends data
        friends_data = request.data.get('friends')
        friends_serializer = UserSerializer(data=friends_data, many=True)
        friends_serializer.is_valid(raise_exception=True)
        friends = friends_serializer.validated_data

        # Create event object
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event = serializer.save()

        # Create event visibility object for each selected friend
        for friend in friends:
            EventVisibility.objects.create(event=event, user=friend)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class EventDetailView(APIView):
    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        if event.creator == request.user or event.visible_to.filter(pk=request.user.pk).exists():
            serializer = EventSerializer(event)
            return Response(serializer.data)
        return Response(status=404)
