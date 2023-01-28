from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .exceptions import AlreadyExistsError
from .forms import CreateFriendShip
from .models import Friend
from ..auth_app.models import WakeAppProfile

UserModel = get_user_model()
UserProfile = WakeAppProfile
from django.views.generic import DetailView


class ViewFriendsView(DetailView):
    template_name = "friend/user_list.html"
    model = Friend
    context_object_name = 'friend_list'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context["friends"] = Friend.objects.friends(self.object)
        return context


class FriendshipAddView(LoginRequiredMixin, CreateView):
    # template_name = "friendship/friend/add.html"
    template_name = 'friendship.html'
    form_class = CreateFriendShip

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            to_user = UserModel.objects.get(username=self.kwargs['to_username'])
            from_user = self.request.user
            try:
                Friend.objects.add_friend(from_user, to_user)
            except AlreadyExistsError as e:
                pass
            return redirect(reverse_lazy("friendship_request_list"))
        return super().dispatch(request, *args, **kwargs)
