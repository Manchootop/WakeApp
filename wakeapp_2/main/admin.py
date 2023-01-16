from django.contrib import admin

from wakeapp_2.main.models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass
