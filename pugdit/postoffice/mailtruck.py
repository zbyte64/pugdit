import eventlet
import ipfsapi
from ipfsapi.exceptions import ErrorResponse, StatusError
from django.conf import settings
import nacl.utils
from nacl.encoding import Base64Encoder as KeyEncoder
from nacl.signing import SigningKey, VerifyKey
import hashlib
import umsgpack
import datetime
import io
import logging
import tempfile
import os

from .models import Post, Identity, Nexus

logger = logging.getLogger(__name__)


def get_client():
    #TODO url read: settings.IPFS_API
    return ipfsapi.connect('ipfs', 5001)

client = get_client()
trucking_pool = eventlet.GreenPool(20)
SERVICE_CREED = b'pugdit net 1'
#TODO precompute without storing
SERVICE_BLOCKNAME = 'QmSiF2Fna3srBzgmvJxB2URBBg7KgxpxDZ9rbHxoXVL5HH'

def find_advertised_peers():
    return client.dht_findprovs(SERVICE_BLOCKNAME)


def put_advertisement():
    #should hash to: settings.SERVICE_BLOCKNAME
    result = client.block_put(io.BytesIO(SERVICE_CREED))
    global SERVICE_BLOCKNAME
    SERVICE_BLOCKNAME = result['Key']
    print('SERVICE_BLOCKNAME:', SERVICE_BLOCKNAME)


def make_fingerprint(public_key):
    s = hashlib.new('sha1', public_key)
    return s.hexdigest()


def retrieve_manifest(node):
    logger.info('retrieving manifest: %s' % node.peer_id)
    robj = client.name_resolve(name=node.peer_id)
    if node.last_manifest_path == robj['Path']:
        return False
    node.last_manifest_path = robj['Path']
    node.save()
    raw_mani = client.cat(robj['Path'])
    return parse_manifest(raw_mani)


def parse_manifest(raw_manifest):
    mani = umsgpack.unpackb(raw_manifest)
    logger.debug('read manifest: %s' % mani)
    assert isinstance(mani, dict)
    assert isinstance(mani['identities'], list)
    assert isinstance(mani['posts'], list)
    identities = dict()
    posts = list()
    manifest = {
        'identities': identities,
        'posts': posts,
    }
    for key, pk in enumerate(mani['identities']):
        ident = {
            'public_key': b64encode(pk),
            'verify_key': VerifyKey(pk),
        }
        identities[key] = ident
    for (smessage, ident_index) in mani['posts']:
        identity = identities[ident_index]
        vk = identity['verify_key']
        to, link = umsgpack.unpackb(vk.verify(smessage))
        posts.append({
            'to': to,
            'link': link,
            'signature': b64encode(smessage),
            'identity': identity,
        })
    return mani


def record_manifest(mani, node=None):
    for env_proto in mani['posts']:
        ident = env_prot['identity']
        try:
            identity = Identity.object.get(public_key=ident['public_key'])
        except Identity.DoesNotExist:
            if node and not node.policy_accept_new_identity():
                continue
            identity = Indentity.objects.create(
                public_key=ident['public_key']
            )
        else:
            if not identity.policy_accept_new_post():
                continue
        envelope = Post.objects.get_or_create(
            to=env_proto['to'],
            link=env_proto['link'],
            signer=identity,
            signature=env_proto['signature'],
        )[0]
        if node:
            envelope.transmitted_nodes.add(node)


def explore_new_routes():
    peers = find_advertised_peers()
    logger.debug('found peers: %s' % peers)
    #async manifest updates
    return trucking_pool.imap(test_peer, peers)


def test_peer(peer):
    if not peer['Responses']:
        return
    peer_id = peer['ID']
    if peer_id == client.id()['ID']:
        return
    node, created = Nexus.objects.get_or_create(peer_id=peer_id,
        defaults={'is_banned': True})
    if created:
        try:
            mani = retrieve_manifest(node)
        except (ValueError, StatusError, ErrorResponse, AssertionError) as error:
            logger.exception(error)
            return #banned
        else:
            record_manifest(mani, node)
            node.is_banned = False
            node.save()
    return node


def drive_route():
    nodes = Nexus.objects.filter(karma__gte=0, is_banned=False)
    return trucking_pool.imap(receive_node, nodes)


def receive_node(node):
    try:
        mani = retrieve_manifest(node)
    except ErrorResponse as error:
        logger.exception(error)
        return
    except (ValueError, StatusError, AssertionError) as error:
        logger.warning(error)
        if node.karma < 100:
            node.karma -= 1
            node.save()
        return
    else:
        record_manifest(mani, node)


def publish_manifest():
    cutoff = datetime.datetime.today() - datetime.timedelta(days=7)
    posts = Post.objects.order_by('-received_timestamp')
    posts = posts.filter(received_timestamp__gte=cutoff, karma__gte=-100)
    posts = posts[:1000]
    mani = {
        'posts': [], #(signed_message, ident_index)
        'identities': [] #(public_key)
    }
    idents = {}
    for post in posts:
        post.verify()
        identity = post.signer
        if identity in idents:
            ident = idents[identity]
        else:
            ident = len(idents)
            idents[identity] = ident
            mani['identities'].append(identity.public_key)
        mani['posts'].append((
            post.signature,
            ident
        ))
    raw_mani = umsgpack.packb(mani)
    logging.info('writing manifest')
    with tempfile.TemporaryDirectory() as tmpdirname:
        mani_path = os.path.join(tmpdirname, 'manifest.mp')
        open(mani_path, 'wb').write(raw_mani)
        #TODO dont assume the first is our file
        #TODO get_path_from_add
        add_result = client.add(mani_path, wrap_with_directory=True)[0]
    ipfs_path = '/ipfs/' + add_result['Hash']
    client.name_publish(ipfs_path)


def mail_route():
    put_advertisement()
    drive_route()
    explore_new_routes()
    trucking_pool.waitall()
    publish_manifest()
