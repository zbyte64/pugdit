from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphene.relay import Node
from graphene import ObjectType, Schema

from .models import Nexus, Identity, Post, Vote
from .forms import PostMarkForm


class NexusNode(DjangoObjectType):
    class Meta:
        model = Nexus
        filter_fields = ['karma', 'is_banned']
        interfaces = (Node, )


class IdentityNode(DjangoObjectType):
    class Meta:
        model = Identity
        filter_fields = ['karma', 'is_banned', 'owner']
        interfaces = (Node, )


class VoteNode(DjangoObjectType):
    class Meta:
        model = Vote
        interfaces = (Node, )


class PostNode(DjangoObjectType):
    #TODO votes
    class Meta:
        model = Post
        filter_fields = ['karma', 'is_pinned', 'to', 'signer', 'received_timestamp']
        interfaces = (Node, )


class Query(ObjectType):
    nexus = Node.Field(NexusNode)
    all_nexus = DjangoFilterConnectionField(NexusNode)

    identity = Node.Field(IdentityNode)
    all_identities = DjangoFilterConnectionField(IdentityNode)

    post = Node.Field(PostNode)
    all_posts = DjangoFilterConnectionField(PostNode)


class PostMarkMutation(DjangoModelFormMutation):
    class Meta:
        form_class = PostMarkForm


class Mutation(ObjectType):
    post = PostMarkMutation.Field()


schema = Schema(query=Query, mutation=Mutation)
