from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from functools import lru_cache

#karma:
# < -100 to ban/ignore
# > 100 to pin forever
# -100 < x < 100 to store temporaly

#CONSIDER: support multi-tenant federated accounts (multiple karma sources problem)


# Create your models here.
class Identity(models.Model):
    public_key = models.TextField(unique=True)
    fingerprint = models.TextField(unique=True) #TODO max length of hash?
    karma = models.IntegerField(default=0)
    is_banned = models.BooleanField(default=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True, null=True,
    )

    topic_subscriptions = ArrayField(
        models.CharField(max_length=10),
        blank=True,
    )

    def __str__(self):
        return self.fingerprint

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


class Nexus(models.Model):
    peer_id = models.CharField(max_length=255, help_text='IPFS identity of the node')
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
    to = models.CharField(max_length=512, db_index=True)
    link = models.CharField(max_length=512, help_text='IPFS url containing the message')
    timestamp = models.CharField(max_length=40) #store as plain text for signature validation purposes

    signer = models.ForeignKey(Identity, related_name='posts', on_delete=models.CASCADE)
    signature = models.TextField()

    received_timestamp = models.DateTimeField(auto_now_add=True)
    transmitted_nexus = models.ManyToManyField(Nexus, blank=True,
        related_name='transmitted_posts', help_text='Nexus(es) that have transmitted this message')
    is_pinned = models.BooleanField(default=False)
    karma = models.IntegerField(default=0)

    class Meta:
        unique_together = [
            ('to', 'link', 'timestamp', 'signer'),
        ]

    def validate_signature(self):
        #TODO
        payload = (to, link, timestamp)
        check_signature(payload, self.identity.public_key, signature)


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        related_name='votes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    karma = models.SmallIntegerField()

    class Meta:
        unique_together = [
            ('user', 'post')
        ]


class Asset(models.Model):
    ipfs_hash = models.CharField(max_length=64, unique=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='pinned_assets')

    def get_absolute_url(self):
        return '/ipfs/' + self.ipfs_hash

    def __str__(self):
        return self.get_absolute_url()
