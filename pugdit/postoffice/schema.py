from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.forms.mutation import DjangoModelFormMutation, DjangoFormMutation
from graphene.relay import Node
from graphene import ObjectType, Schema, Field
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

from .models import Nexus, Identity, Post, Vote
from .forms import PostMarkForm, RegisterIdentityForm


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


class AuthUserNode(DjangoObjectType):
    class Meta:
        model = User


class VoteNode(DjangoObjectType):
    class Meta:
        model = Vote
        interfaces = (Node, )


class PostNode(DjangoObjectType):
    #TODO votes
    class Meta:
        model = Post
        filter_fields = {
            'karma': ['lte', 'gte'],
            'is_pinned': ['exact'],
            'to': ['startswith', 'exact'],
            'signer': ['exact'],
            'received_timestamp': ['lte', 'gte'],
        }
        interfaces = (Node, )


class Query(ObjectType):
    auth_user = Field(AuthUserNode)
    nexus = Node.Field(NexusNode)
    all_nexus = DjangoFilterConnectionField(NexusNode)

    identity = Node.Field(IdentityNode)
    all_identities = DjangoFilterConnectionField(IdentityNode)

    post = Node.Field(PostNode)
    all_posts = DjangoFilterConnectionField(PostNode, order_by=['to', '-received_timestamp'])

    def resolve_auth_user(self, info, **kwargs):
        user = info.context.user
        if not user.is_authenticated:
            return None
        return user


class PostMarkMutation(DjangoModelFormMutation):
    class Meta:
        form_class = PostMarkForm

    @classmethod
    def get_form_kwargs(cls, root, info, **input):
        kwargs = {"data": input}
        return kwargs


class RegisterIdentityMutation(DjangoModelFormMutation):
    class Meta:
        form_class = RegisterIdentityForm

    @classmethod
    def get_form_kwargs(cls, root, info, **input):
        kwargs = {"data": input}
        kwargs['owner'] = info.context.user
        return kwargs


class AuthenticationMutation(DjangoFormMutation):
    class Meta:
        form_class = AuthenticationForm

    @classmethod
    def get_form_kwargs(cls, root, info, **input):
        kwargs = {"data": input}
        kwargs['request'] = info.context
        return kwargs

    @classmethod
    def perform_mutate(cls, form, info):
        obj = form.get_user()
        login(form.request, obj)
        #kwargs = {'authUser': obj}
        return cls(errors=[])#, **kwargs)


class Mutation(ObjectType):
    authentication = AuthenticationMutation.Field()
    post_mark = PostMarkMutation.Field()
    register_identity = RegisterIdentityMutation.Field()


schema = Schema(query=Query, mutation=Mutation)
