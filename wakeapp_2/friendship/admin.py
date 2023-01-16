from django.contrib import admin

from wakeapp_2.friendship.models import Friendship


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    pass
