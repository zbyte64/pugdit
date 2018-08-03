from django.db import models
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
    fingerprint = models.TextField(unique=True)
    karma = models.IntegerField(default=0)
    is_banned = models.BooleanField(default=False)

    topic_subscriptions = ArrayField(
        models.CharField(max_length=10),
        blank=True,
    )

    voted_posts = models.ManyToManyField('SignedEnvelope', through='Vote',
        related_name='voted_identities', blank=True)
    friends = models.ManyToManyField('Identity',
        related_name='followers', blank=True)

    @property
    def subscribed_posts(self):
        posts = SignedEnvelope.objects.none()
        for topic in self.topic_subscriptions:
            #TODO SignedEnvelope.objects.for_topics(*)
            posts |= SignedEnvelope.objects.filter(to__startswith=topic+'/')
        return posts

    def policy_accept_new_post(self):
        if self.karma < -100:
            return False
        return True


class Node(models.Model):
    peer_id = models.CharField(max_length=255, help_text='IPFS identity of the node')
    karma = models.IntegerField(default=0)
    is_banned = models.BooleanField(default=False)
    last_manifest_path = models.CharField(max_length=255, blank=True)

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


#TODO rename to SignedPost or Post
class SignedEnvelope(models.Model):
    to = models.CharField(max_length=512, db_index=True)
    link = models.CharField(max_length=512, help_text='IPFS url containing the message')
    timestamp = models.CharField(max_length=40) #store as plain text for signature validation purposes

    signer = models.ForeignKey(Identity, related_name='posts', on_delete=models.CASCADE)
    signature = models.TextField()

    received_timestamp = models.DateTimeField(auto_now_add=True)
    transmitted_nodes = models.ManyToManyField(Node, blank=True,
        related_name='transmitted_posts', help_text='Nodes that have transmitted this message')
    pinned = models.BooleanField(default=False)
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
    identity = models.ForeignKey(Identity, related_name='votes', on_delete=models.CASCADE)
    post = models.ForeignKey(SignedEnvelope, on_delete=models.CASCADE)
    karma = models.SmallIntegerField()

    class Meta:
        unique_together = [
            ('identity', 'post')
        ]
