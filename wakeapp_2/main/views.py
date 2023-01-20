from django.shortcuts import render, get_object_or_404
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import CreateView, DetailView, TemplateView

from wakeapp_2.main.models import Event, EventVisibility
from wakeapp_2.main.serializers import EventSerializer, UserSerializer


class DashboardView(TemplateView):
    template_name = 'main/dashboard.html'


# class CreateEventView(generics.CreateAPIView):
#     renderer_classes = [BrowsableAPIRenderer]
#     serializer_class = EventSerializer
#
#     def post(self, request, *args, **kwargs):
#         # Validate and deserialize the friends data
#         friends_data = request.data.get('friends')
#         friends_serializer = UserSerializer(data=friends_data, many=True)
#         friends_serializer.is_valid(raise_exception=True)
#         friends = friends_serializer.validated_data
#
#         # Create event object
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         event = serializer.save()
#
#         # Create event visibility object for each selected friend
#         for friend in friends:
#             EventVisibility.objects.create(event=event, user=friend)
#
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#
#
# class EventDetailView(APIView):
#     def get(self, request, pk):
#         event = get_object_or_404(Event, pk=pk)
#         if event.creator == request.user or event.visible_to.filter(pk=request.user.pk).exists():
#             serializer = EventSerializer(event)
#             return Response(serializer.data)
#         return Response(status=404)


from django.urls import reverse_lazy
from django.shortcuts import render


class CreateEventView(CreateView):
    model = Event
    fields = ('name', 'visible_to', 'location', 'date', 'friends')
    template_name = 'event_form.html'
    success_url = reverse_lazy('event_detail')

    def form_valid(self, form):
        friends_data = self.request.POST.getlist('friends')
        friends = []
        for friend_data in friends_data:
            friend_serializer = UserSerializer(data=friend_data)
            friend_serializer.is_valid(raise_exception=True)
            friends.append(friend_serializer.validated_data)

        response = super().form_valid(form)

        for friend in friends:
            EventVisibility.objects.create(event=self.object, user=friend)

        return response


class EventDetailView(DetailView):
    model = Event
    template_name = 'event_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.creator == request.user or self.object.visible_to.filter(pk=request.user.pk).exists():
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        return render(request, '404.html', status=404)
