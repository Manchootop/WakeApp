from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView
from .exceptions import AlreadyExistsError
from .models import Friend
from .. import settings
from ..auth_app.models import WakeAppProfile

UserModel = get_user_model()
UserProfile = WakeAppProfile
from django.views.generic import DetailView


def get_friendship_context_object_name():
    return getattr(settings, "FRIENDSHIP_CONTEXT_OBJECT_NAME", "user")


class ViewFriendsView(DetailView):
    # template_name = "friendship/friend/user_list.html"
    template_name = 'friendship.html'
    model = Friend
    context_object_name = get_friendship_context_object_name()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context["friends"] = Friend.objects.friends(self.object)
        context["friendship_context_object_name"] = get_friendship_context_object_name()
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, username=self.kwargs['username'])


class FriendshipAddView(LoginRequiredMixin, CreateView):
    # template_name = "friendship/friend/add.html"
    template_name = 'friendship.html'
    form_class = None

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            to_user = UserModel.objects.get(username=self.kwargs['to_username'])
            from_user = self.request.user
            try:
                Friend.objects.add_friend(from_user, to_user)
            except AlreadyExistsError as e:
                pass
            return redirect(reverse("friendship_request_list"))
        return super().dispatch(request, *args, **kwargs)
