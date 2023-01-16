from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from .forms import FriendshipRequestForm
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


class FriendshipView(LoginRequiredMixin, ListView):
    model = Friendship
    template_name = 'friendship.html'
    serializer_class = FriendshipSerializer

    def get_queryset(self):
        friendships = Friendship.objects.filter(Q(sender=self.request.user) | Q(receiver=self.request.user))
        return friendships.filter(status='accepted')


# class SendFriendshipRequestView(viewsets.ViewSet):
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def create(self, request):
#         # Get the user that the request is being sent to
#         receiver = UserModel.objects.get(id=request.data['receiver'])
#
#         # Create a new friendship with a status of 'pending'
#         friendship = Friendship.objects.create(
#             sender=request.user,
#             receiver=receiver,
#             status='pending'
#         )
#
#         serializer = FriendshipSerializer(friendship)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# class SendFriendshipRequestView(LoginRequiredMixin, FormView):
#     form_class = SendFriendshipRequestForm
#     template_name = 'send_friendship_request.html'
#
#     def form_valid(self, form):
#         receiver = form.cleaned_data['receiver']
#         Friendship.objects.create(
#             sender=self.request.user,
#             receiver=receiver,
#             status='pending'
#         )
#         return render(self.request, 'friendship_request_sent.html')

# class AcceptRejectFriendshipRequestView(LoginRequiredMixin, View):
#     def post(self, request, pk):
#         friendship = get_object_or_404(Friendship, pk=pk)
#         form = AcceptRejectFriendshipRequestForm(request.POST)
#         if form.is_valid():
#             if friendship.receiver != request.user:
#                 return render(request, 'error.html', {'message': 'You are not authorized to perform this action'})
#             friendship.status = form.cleaned_data['status']
#             friendship.save()
#             return render(request, 'friendship_request_updated.html')
#         else:
#             return render(request, 'error.html', {'message': 'Invalid form data'})


class SendFriendshipRequestView(LoginRequiredMixin, CreateView):
    model = Friendship
    form_class = FriendshipRequestForm
    template_name = 'send_friendship_request.html'
    success_url = reverse_lazy('friendship_request_sent')

    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.instance.status = 'pending'
        return super().form_valid(form)


class AcceptRejectFriendshipRequestView(LoginRequiredMixin, UpdateView):
    model = Friendship
    form_class = FriendshipRequestForm
    template_name = 'accept_reject_friendship_request.html'
    success_url = reverse_lazy('friendship_request_updated')

    def form_valid(self, form):
        if form.instance.receiver != self.request.user:
            return render(self.request, 'error.html', {'message': 'You are not authorized to perform this action'})
        return super().form_valid(form)


# class AcceptFriendshipRequestView(viewsets.ViewSet):
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def update(self, request, pk=None):
#         # Get the friendship request
#         friendship = Friendship.objects.get(id=pk)
#
#         # Ensure that the request is being accepted by the intended receiver
#         if friendship.receiver != request.user:
#             return Response(status=status.HTTP_403_FORBIDDEN)
#
#         # Update the status of the request to 'accepted'
#         friendship.status = 'accepted'
#         friendship.save()
#
#         serializer = FriendshipSerializer(friendship)
#         return Response(serializer.data, status=status.HTTP_200_OK)


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
