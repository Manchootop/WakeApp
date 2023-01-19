from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from .forms import FriendshipRequestForm
from .models import FriendshipRequest, Friend
from .serializers import FriendshipSerializer
from .. import settings
from ..auth_app.models import WakeAppProfile

UserModel = get_user_model()
UserProfile = WakeAppProfile
from django.views.generic import DetailView
from django.contrib.auth import get_user_model


def get_friendship_context_object_name():
    return getattr(settings, "FRIENDSHIP_CONTEXT_OBJECT_NAME", "user")


class ListFriendsView(ListView):
    model = Friend
    # template_name = "friendship/friend/user_list.html"
    template_name = 'friendship.html'
    context_object_name = 'user'

    def get_queryset(self):
        user = get_object_or_404(UserProfile, user=self.request.user)
        return Friend.objects.friends(user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["friendship_context_object_name"] = get_friendship_context_object_name()
        context['user'] = get_object_or_404(UserProfile, user=self.kwargs['user'])
        '''
        Assigns the user object to the context variable 'user' by looking up the UserModel by the user attribute of the request object, which is the currently logged in user and returns a 404 error if the object is not found.
        '''
        return context


from django.views.generic import FormView
from django.urls import reverse


# from friendship.models import AlreadyExistsError


class AlreadyExistsError:
    pass


@login_required
def friendship_add_friend(
        request, to_username, template_name="friendship/friend/add.html"
):
    context = {"to_username": to_username}

    if request.method == "POST":
        to_user = UserModel.objects.get(username=to_username)
        from_user = request.user
        try:
            Friend.objects.add_friend(from_user, to_user)
        except AlreadyExistsError as e:
            # context["errors"] = ["%s" % e]
            pass
        else:
            # return redirect("friendship_request_list")
            return redirect('/#')
        # TODO fix this redirect
    return render(request, template_name, context)


class FriendshipViewSet(viewsets.ModelViewSet):
    serializer_class = FriendshipSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        # Get the list of friendships where the user is the sender or receiver
        friendships = FriendshipRequest.objects.filter(Q(sender=self.request.user) | Q(receiver=self.request.user))

        # Filter the friendships to only include accepted ones
        return friendships.filter(status='accepted')


class FriendshipView(LoginRequiredMixin, ListView):
    model = FriendshipRequest
    template_name = 'friendship.html'
    serializer_class = FriendshipSerializer

    def get_queryset(self):
        friendships = FriendshipRequest.objects.filter(Q(sender=self.request.user) | Q(receiver=self.request.user))
        return friendships.filter(status='accepted')


# class SendFriendshipRequestView(viewsets.ViewSet):
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def create(self, request):
#         # Get the user that the request is being sent to
#         receiver = UserModel.objects.get(id=request.data['receiver'])
#
#         # Create a new friendship with a status of 'pending'
#         friendship = FriendshipRequest.objects.create(
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
#         FriendshipRequest.objects.create(
#             sender=self.request.user,
#             receiver=receiver,
#             status='pending'
#         )
#         return render(self.request, 'friendship_request_sent.html')

# class AcceptRejectFriendshipRequestView(LoginRequiredMixin, View):
#     def post(self, request, pk):
#         friendship = get_object_or_404(FriendshipRequest, pk=pk)
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
    model = FriendshipRequest
    form_class = FriendshipRequestForm
    template_name = 'send_friendship_request.html'
    success_url = reverse_lazy('friendship_request_sent')

    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.instance.status = 'pending'
        return super().form_valid(form)


class AcceptRejectFriendshipRequestView(LoginRequiredMixin, UpdateView):
    model = FriendshipRequest
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
#         friendship = FriendshipRequest.objects.get(id=pk)
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
        friendship = FriendshipRequest.objects.get(id=pk)

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
