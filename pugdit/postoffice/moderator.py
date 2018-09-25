from moderation import moderation
from moderation.moderator import GenericModerator
from moderation.db import ModeratedModel

from .models import Nexus, Post, Identity


class NexusModerator(GenericModerator):
    auto_reject_for_groups = ['banned']
    visibility_column = 'is_public'


class PostModerator(GenericModerator):
    auto_reject_for_groups = ['banned']
    visibility_column = 'is_public'


class IdentityModerator(GenericModerator):
    auto_reject_for_groups = ['banned']
    visibility_column = 'is_public'


moderation.register(Post, PostModerator)
moderation.register(Nexus, NexusModerator)
moderation.register(Identity, IdentityModerator)
