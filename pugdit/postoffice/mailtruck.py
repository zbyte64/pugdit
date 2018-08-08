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
SERVICE_BLOCKNAME = None

def find_advertised_peers():
    return client.dht_findprovs(SERVICE_BLOCKNAME)


def put_advertisement():
    #should hash to: settings.SERVICE_BLOCKNAME
    result = client.block_put(io.BytesIO(SERVICE_CREED))
    global SERVICE_BLOCKNAME
    SERVICE_BLOCKNAME = result['Key']


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


def check_signature(env, verify_key):
    smessage = ','.join((env['to'], env['link'], env['timestamp']))
    smessage = smessage.encode('utf8')
    verify_key.verify(smessage, env['signature'])


def parse_manifest(raw_manifest):
    mani = umsgpack.unpackb(raw_manifest)
    logger.debug('read manifest: %s' % mani)
    assert isinstance(mani, dict)
    assert isinstance(mani['identities'], dict)
    assert isinstance(mani['posts'], list)
    for ident in mani['identities'].values():
        pk = ident['public_key']
        ident['verify_key'] = VerifyKey(pk, KeyEncoder)
        ident['fingerprint'] = make_fingerprint(pk)
    for env in mani['posts']:
        vk = mani['identities'][env['identity']]['verify_key']
        check_signature(env, vk)
    return mani


def record_manifest(mani, node=None):
    for env_proto in mani['posts']:
        ident = mani['identities'][env_proto['identity']]
        try:
            identity = Identity.object.get(fingerprint=ident['fingerprint'])
        except Identity.DoesNotExist:
            if node and not node.policy_accept_new_identity():
                continue
            identity = Indentity.objects.create(
                public_key=ident['public_key'],
                fingerprint=ident['fingerprint']
            )
        else:
            if not identity.policy_accept_new_post():
                continue
        envelope = Post.objects.get_or_create(
            to=env_proto['to'],
            link=env_proto['link'],
            timestamp=env_proto['timestamp'],
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
        'posts': [],
        'identities': {}
    }
    idents = {}
    for post in posts:
        identity = post.identity
        if identity in idents:
            ident = idents[identity]
        else:
            ident = len(idents)
            idents[identity] = ident
            mani['identities'][ident] = {
                'public_key': identity.public_key
            }
        mani['posts'].append({
            'to': post.to,
            'link': post.link,
            'timestamp': post.timestamp,
            'signature': post.signature,
            'identity': ident
        })
    raw_mani = umsgpack.packb(mani)
    logging.info('writing manifest')
    with tempfile.TemporaryDirectory() as tmpdirname:
        mani_path = os.path.join(tmpdirname, 'manifest.msg')
        open(mani_path, 'wb').write(raw_mani)
        add_result = client.add(mani_path)
    ipfs_path = '/ipfs/' + add_result['Hash']
    client.name_publish(ipfs_path)


def mail_route():
    put_advertisement()
    drive_route()
    explore_new_routes()
    trucking_pool.waitall()
    publish_manifest()
