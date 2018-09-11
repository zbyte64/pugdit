from django.contrib import admin
from .models import Nexus, Identity, Post


class NexusAdmin(admin.ModelAdmin):
    list_display = ['peer_id', 'last_manifest_path', 'is_banned', 'karma']
    list_filter = ['is_banned']
admin.site.register(Nexus, NexusAdmin)


class IdentityAdmin(admin.ModelAdmin):
    pass
admin.site.register(Identity, IdentityAdmin)


def make_pinned(modeladmin, request, queryset):
    #TODO do as a task
    for post in queryset:
        post.clean()
        post.pin()
        post.save()
make_pinned.short_description = 'Pin selected posts'


class PostAdmin(admin.ModelAdmin):
    list_display = ['address', 'karma', 'is_pinned']
    list_filter = ['is_pinned', 'received_timestamp']
    actions = [make_pinned]
admin.site.register(Post, PostAdmin)
