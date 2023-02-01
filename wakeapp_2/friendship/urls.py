from django.urls import path

# from wakeapp_2.friendship.views import SendFriendshipRequestView, AcceptFriendshipRequestView, \
#     RejectFriendshipRequestView, FriendshipViewSet

# urlpatterns = [
# path('friends/', FriendshipViewSet.as_view({'get': 'list'}), name='friends'),
# path('friendship-requests/', SendFriendshipRequestView.as_view({'post': 'create'}), name='send_friendship_request'),
# path('friendship-requests/<int:pk>/accept/', AcceptFriendshipRequestView.as_view({'put': 'update'}),
#      name='accept_friendship_request'),
# path('friendship-requests/<int:pk>/reject/', RejectFriendshipRequestView.as_view({'put': 'update'}),
#      name='reject_friendship_request'),
# ]
from wakeapp_2.friendship.views import AddFriendView, FriendshipCancelView, \
    FriendshipAcceptRejectView, UserSearchView

urlpatterns = [
    path('add/<int:pk>/', AddFriendView.as_view(), name='add friend'),
    path('cancel/<int:friendship_request_id>/', FriendshipCancelView.as_view(), name='friendship_cancel'),
    path('accept_or_reject/<int:friendship_request_id>/', FriendshipAcceptRejectView.as_view(),
         name='friendship_accept_or_reject'),
    path('search_user/', UserSearchView.as_view(), name='search_user')
]

'''
from django.urls import reverse

# Generate the URL for the 'friends' view
friends_url = reverse('friends')

# Generate the URL for the 'send_friendship_request' view
send_request_url = reverse('send_friendship_request')

# Generate the URL for the 'accept_friendship_request' view
accept_request_url = reverse('accept_friendship_request', kwargs={'pk': 123})

# Generate the URL for the 'reject_friendship_request' view
reject_request_url = reverse('reject_friendship_request', kwargs={'pk': 123})
'''
