from django.contrib import admin
from moderation.admin import ModerationAdmin
from .models import Nexus, Identity, Post


class NexusAdmin(ModerationAdmin):
    list_display = ['peer_id', 'last_manifest_path', 'is_public', 'karma']
    list_filter = ['is_public']
admin.site.register(Nexus, NexusAdmin)


class IdentityAdmin(ModerationAdmin):
    list_filter = ['is_public']
admin.site.register(Identity, IdentityAdmin)


def make_pinned(modeladmin, request, queryset):
    #TODO do as a task
    for post in queryset:
        post.clean()
        post.pin()
        post.save()
make_pinned.short_description = 'Pin selected posts'


class PostAdmin(ModerationAdmin):
    list_display = ['address', 'karma', 'is_pinned']
    list_filter = ['is_pinned', 'received_timestamp', 'is_public']
    actions = [make_pinned]
admin.site.register(Post, PostAdmin)
