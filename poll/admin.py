from django.contrib import admin

from poll.models import Choice, Poll, Vote


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_filter = ("author",)
    date_hierarchy = "published"


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    pass


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    pass
