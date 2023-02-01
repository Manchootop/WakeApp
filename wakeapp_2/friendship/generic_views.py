from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic as generic_views
from .exceptions import AlreadyExistsError
from .models import Friend, FriendshipRequest
from ..auth_app.models import WakeAppProfile

UserModel = get_user_model()
UserProfile = WakeAppProfile


class AddFriendView(LoginRequiredMixin, generic_views.CreateView):
    template_name = "friend/add.html"
    # template_name = 'friendship.html'
    form_class = CreateFriendShip
    model = FriendshipRequest

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