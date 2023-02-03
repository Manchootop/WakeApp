from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic as generic_views
from .exceptions import AlreadyExistsError
# from .forms import CreateFriendShip
from .models import Friend, FriendshipRequest
from ..auth_app.models import WakeAppProfile

UserModel = get_user_model()
UserProfile = WakeAppProfile


class ViewFriendView(generic_views.DetailView):
    template_name = "friend/user_list.html"
    model = Friend
    context_object_name = 'friend_list'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context["friends"] = Friend.objects.friends(self.object)
        return context


class AddFriendView(LoginRequiredMixin, generic_views.CreateView):
    template_name = "friend/add.html"
    # template_name = 'friendship.html'
    # form_class = CreateFriendShip
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


class UserSearchView(generic_views.View):
    template_name = 'friendship/search_results.html'

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        users = UserModel.objects.filter(username__icontains=query)
        return render(request, self.template_name, {'users': users})


class FriendshipAcceptRejectView(generic_views.FormView, LoginRequiredMixin):
    http_method_names = ['post']
    template_name = 'friend/accept_reject_friendship_request.html'

    def form_valid(self, form):
        friendship_request_id = self.kwargs['friendship_request_id']
        f_request = get_object_or_404(
            self.request.user.friendship_requests_received, id=friendship_request_id
            # friendship_requests_received --> related name to to_user "sender"
        )
        action = self.request.POST.get("action")
        if action == "accept":
            f_request.accept()
        elif action == "reject":
            f_request.reject()
        return redirect("friendship_view_friends")

    def form_invalid(self, form):
        friendship_request_id = self.kwargs['friendship_request_id']
        return redirect(
            "friendship_requests_detail", friendship_request_id=friendship_request_id
        )


# @login_required
# def friendship_cancel(request, friendship_request_id):
#     """Cancel a previously created friendship_request_id"""
#     if request.method == "POST":
#         f_request = get_object_or_404(
#             request.user.friendship_requests_sent, id=friendship_request_id
#         )
#         f_request.cancel()
#         return redirect("friendship_request_list")
#
#     return redirect(
#         "friendship_requests_detail", friendship_request_id=friendship_request_id
#     )


class FriendshipCancelView(LoginRequiredMixin, generic_views.View):
    @staticmethod
    def post(self, request, friendship_request_id):
        f_request = get_object_or_404(
            request.user.friendship_requests_sent, id=friendship_request_id
        )
        f_request.cancel()
        return redirect("friendship_request_list")

    @staticmethod
    def get(self, request, friendship_request_id):
        return redirect(
            "friendship_requests_detail", friendship_request_id=friendship_request_id
        )


@login_required
def friendship_request_list(
        request, template_name="friendship/friend/requests_list.html"
):
    """View unread and read friendship requests"""
    friendship_requests = Friend.objects.requests(request.user)
    # This shows all friendship requests in the database
    # friendship_requests = FriendshipRequest.objects.filter(rejected__isnull=True)

    return render(request, template_name, {"requests": friendship_requests})


@login_required
def friendship_request_list_rejected(
        request, template_name="friendship/friend/requests_list.html"
):
    """View rejected friendship requests"""
    # friendship_requests = Friend.objects.rejected_requests(request.user)
    friendship_requests = FriendshipRequest.objects.filter(rejected__isnull=False)

    return render(request, template_name, {"requests": friendship_requests})


@login_required
def friendship_requests_detail(
        request, friendship_request_id, template_name="friendship/friend/request.html"
):
    """View a particular friendship request"""
    f_request = get_object_or_404(FriendshipRequest, id=friendship_request_id)

    return render(request, template_name, {"friendship_request": f_request})


class ListFriendsView(generic_views.ListView):
    model = Friend
    template_name = 'friend/list_friends.html'
    context_object_name = 'friends'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friends'] = context['friends'].filter(to_user__accepted=self.request.user)
        context['count'] = context['friends'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['friends'] = context['friends'].filter(title__icontains=search_input)

        context['search_input'] = search_input

        return context
