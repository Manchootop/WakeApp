from django.contrib import admin

# from wakeapp_2.friendship.models import FriendshipRequest
from wakeapp_2.friendship.models import Friend


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    pass
