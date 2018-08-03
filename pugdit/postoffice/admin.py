from django.contrib import admin
from .models import Nexus, Identity, Post


class NexusAdmin(admin.ModelAdmin):
    pass
admin.site.register(Nexus, NexusAdmin)


class IdentityAdmin(admin.ModelAdmin):
    pass
admin.site.register(Identity, IdentityAdmin)


class PostAdmin(admin.ModelAdmin):
    pass
admin.site.register(Post, PostAdmin)
