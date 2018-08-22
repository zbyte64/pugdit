from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from nacl.signing import VerifyKey
from base64 import b64decode, standard_b64encode, standard_b64decode
from functools import lru_cache

#karma:
# < -100 to ban/ignore
# > 100 to pin forever
# -100 < x < 100 to store temporaly

#CONSIDER: support multi-tenant federated accounts (multiple karma sources problem)


# Create your models here.
class Identity(models.Model):
    public_key = models.CharField(max_length=77, unique=True, help_text="Base64 encoded key for verifying signatures")
    karma = models.IntegerField(default=0)
    is_banned = models.BooleanField(default=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True, null=True,
    )

    topic_subscriptions = ArrayField(
        models.CharField(max_length=10),
        blank=True, default=list,
    )

    def __str__(self):
        return self.public_key

    #TODO proper user <-> identity decouple
    #voted_posts = models.ManyToManyField('Post', through='Vote',
    #    related_name='voted_identities', blank=True)
    #friends = models.ManyToManyField('Identity',
    #    related_name='followers', blank=True)

    @property
    def subscribed_posts(self):
        posts = Post.objects.none()
        for topic in self.topic_subscriptions:
            #TODO Post.objects.for_topics(*)
            posts |= Post.objects.filter(to__startswith=topic+'/')
        return posts

    def policy_accept_new_post(self):
        if self.karma < -100:
            return False
        return True

    @property
    def verify_key(self):
        return VerifyKey(b64decode(self.public_key.encode('utf8')))

    def verify(self, smessage):
        return self.verify_key.verify(smessage)


class Nexus(models.Model):
    peer_id = models.CharField(max_length=46, help_text='IPFS identity of the node')
    karma = models.IntegerField(default=0)
    is_banned = models.BooleanField(default=False)
    last_manifest_path = models.CharField(max_length=255, blank=True)
    last_sync = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.peer_id

    @lru_cache()
    def _message_health_stats(self):
        return self.transmitted_posts.all().aggregate(
            volume=Count('id'),
            avg_karma=Avg('karma'),
        )

    def policy_accept_new_identity(self):
        if self.karma < -10:
            return False
        if self.karma > 100:
            return True
        stats = self._message_health_stats()
        if state['avg_karma'] > .5:
            return True
        if stats['avg_karma'] + self.karma < 0:
            return False
        if stats['volume'] > 100:
            return False
        return True


class Post(models.Model):
    to = models.CharField(max_length=512)
    link = models.CharField(max_length=255, help_text='IPFS url containing the message')

    signer = models.ForeignKey(Identity, related_name='posts', on_delete=models.CASCADE)
    signature = models.CharField(max_length=1024)

    received_timestamp = models.DateTimeField(auto_now_add=True)
    transmitted_nexus = models.ManyToManyField(Nexus, blank=True,
        related_name='transmitted_posts', help_text='Nexus(es) that have transmitted this message')
    is_pinned = models.BooleanField(default=False)
    karma = models.IntegerField(default=0)
    chain_level = models.SmallIntegerField(default=0, db_index=True)
    address = models.CharField(max_length=576, db_index=True, blank=True)

    class Meta:
        unique_together = [
            ('to', 'link', 'signer'),
        ]

    def __str__(self):
        return self.signature

    def clean(self):
        print('cleaning')
        assert self.to, 'to must be set'
        self.chain_level = self.to.count('/')
        response_id = standard_b64decode(self.signature)[:32]
        self.address = '%s/%s' % (self.to, standard_b64encode(response_id).decode('utf8'))
        print('cleaned', self.address)

    def verify(self):
        self.signer.verify(b64decode(self.signature))



class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        related_name='votes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    karma = models.SmallIntegerField(default=0)

    class Meta:
        unique_together = [
            ('user', 'post')
        ]


class Asset(models.Model):
    ipfs_hash = models.CharField(max_length=46, unique=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='pinned_assets')
    ipfs_paths = ArrayField(
        models.CharField(max_length=255),
        blank=True, default=list,
    )

    def get_absolute_url(self):
        return '/ipfs/' + self.ipfs_hash

    def __str__(self):
        return self.get_absolute_url()
