import eventlet
import ipfsapi
from ipfsapi.exceptions import ErrorResponse, StatusError
from django.conf import settings
from django.db import close_old_connections
import nacl.utils
from nacl.encoding import Base64Encoder as KeyEncoder
from nacl.signing import SigningKey, VerifyKey
from base64 import b64encode, b64decode
import hashlib
import umsgpack
import datetime
import io
import logging
import tempfile
import os
import requests

from .models import Post, Identity, Nexus

logger = logging.getLogger(__name__)


def log_fail(error, prefix=None):
    if hasattr(error, 'original'):
        if hasattr(error.original, 'response'):
            error = error.original.response.json()
    if prefix:
        logger.warning('[%s] %s' % (prefix, error))
    else:
        logger.warning(str(error))

def get_client():
    #TODO url read: settings.IPFS_API
    return ipfsapi.connect('ipfs', 5001)

client = get_client()
trucking_pool = eventlet.GreenPool(settings.TRUCK_FLEET_SIZE)
SERVICE_CREED = b'pugdit net 1'
SERVICE_BLOCKNAME = settings.SERVICE_BLOCKNAME


def find_advertised_peers():
    lines = client.dht_findprovs(SERVICE_BLOCKNAME)
    for line in filter(lambda x: x.get('Type') == 4, lines):
        for r in (line['Responses'] or []):
            if r['Addrs']:
                yield r


def put_advertisement():
    #should hash to: settings.SERVICE_BLOCKNAME
    result = client.block_put(io.BytesIO(SERVICE_CREED))
    assert SERVICE_BLOCKNAME == result['Key']
    logger.info('SERVICE_BLOCKNAME: %s' % SERVICE_BLOCKNAME)


def make_fingerprint(public_key):
    s = hashlib.new('sha1', public_key)
    return s.hexdigest()


def store_filepath(filepath):
    '''
    Stores a file with it's filename
    Returns the dagnode of the file with a `Path` key
    '''
    add_results = client.add(filepath, wrap_with_directory=True)
    logger.debug('add_results: %s' % add_results)
    path = [o['Name'] or o['Hash'] for o in add_results]
    ipfs_path = '/ipfs/' + '/'.join(reversed(path))
    add_result = add_results[0]
    add_result['Path'] = ipfs_path
    return add_result


def retrieve_manifest(node):
    logger.info('[%s] retrieve manifest' % node.peer_id)
    # no penalty for not resolving?
    robj = client.name_resolve(name=node.peer_id)
    path = robj['Path']
    logger.info('[%s] resolved: %s' % (node.peer_id, path))
    assert path.endswith('manifest.mp'), 'Not a manifest file'
    if node.last_manifest_path == path:
        pass
        #return False
    else:
        #TODO update after sync?
        node.last_manifest_path = path
        node.save()
    response = requests.get(settings.IPFS_URL + path)
    response.raise_for_status()
    raw_mani = response.content
    return parse_manifest(raw_mani)


def parse_manifest(raw_manifest):
    mani = umsgpack.unpackb(raw_manifest)
    logger.debug('read manifest: %s' % mani)
    assert isinstance(mani, dict), 'Manifest is not a dictionary'
    assert isinstance(mani['identities'], list), 'Manifest is missing identities'
    assert isinstance(mani['posts'], list), 'Manifest is missing posts'
    return transform_manifest(mani)

#TODO better name, creates a linked manifset with key objects
def transform_manifest(mani):
    identities = dict()
    posts = list()
    manifest = {
        'identities': identities,
        'posts': posts,
    }
    for key, pk in enumerate(mani['identities']):
        ident = {
            'public_key': pk, #b64encode(pk),
            'verify_key': VerifyKey(b64decode(pk)),
        }
        identities[key] = ident
    for (smessage, ident_index) in mani['posts']:
        identity = identities[ident_index]
        vk = identity['verify_key']
        mpacked = vk.verify(b64decode(smessage))
        to, link = umsgpack.unpackb(mpacked)
        posts.append({
            'to': to,
            'link': link,
            'signature': smessage,
            'identity': identity,
        })
    return manifest


def record_manifest(mani, node=None):
    if node:
        logger.info('[%s] recording manifest' % node.peer_id)
    for env_proto in mani['posts']:
        ident = env_proto['identity']
        #TODO optimize call based on node policy
        try:
            identity = Identity.objects.get(public_key=ident['public_key'])
        except Identity.DoesNotExist:
            if node and not node.policy_accept_new_identity():
                logger.warn('identity rejected')
                continue
            identity = Identity.objects.create(
                public_key=ident['public_key']
            )
        else:
            if not identity.policy_accept_new_post():
                logger.warn('post rejected')
                continue
        envelope, _c = Post.objects.get_or_create(
            to=env_proto['to'],
            link=env_proto['link'],
            signer=identity,
            signature=env_proto['signature'],
        )
        if node:
            envelope.transmitted_nexus.add(node)
        if _c:
            post.clean()
            post.pin()
            post.save()
            logger.debug('new post: %s' % envelope)


def knock_knock_node(node):
    try:
        mani = retrieve_manifest(node)
    except StatusError as error:
        log_fail(error, node.peer_id)
        reason = error.original.response.json().get('Message')
        if reason == 'could not resolve name':
            return False, "NOT_PUBLISHED"
        elif reason == 'this dag node is a directory':
            return False, 'BAD_MANIFEST'
        return False, "UNAVAILABLE"
    except (ValueError, AssertionError) as error:
        log_fail(error, node.peer_id)
        return False, 'BAD_MANIFEST'
    except (requests.exceptions.HTTPError) as error:
        #TODO
        log_fail(error, node.peer_id)
        return False, 'UNAVAILABLE'
    else:
        if mani:
            record_manifest(mani, node)
            return True, ''
        return False, 'BAD_MANIFEST'


def test_peer(peer):
    peer_id = peer['ID']
    if not peer_id:
        return
    if peer_id == client.id()['ID']:
        return
    node, created = Nexus.objects.get_or_create(peer_id=peer_id,
        defaults={'is_banned': True})
    if created:
        success, code = knock_knock_node(node)
        if success:
            node.karma = 1
            node.is_banned = False
            node.save()
        elif code == 'UNAVAILABLE':
            node.is_banned = False
            node.karma = -1
            node.save()
    return node


def clean_exec(fn):
    def foo(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        finally:
            close_old_connections()
    return foo


def explore_new_routes():
    peers = list(find_advertised_peers())
    logger.debug('found peers: %s' % len(peers))
    #async manifest updates
    return list(trucking_pool.imap(clean_exec(test_peer), peers))


def drive_route():
    nodes = Nexus.objects.filter(karma__gte=-10, is_banned=False)
    return list(trucking_pool.imap(clean_exec(receive_node), nodes))


def receive_node(node):
    success, code = knock_knock_node(node)
    if success:
        if node.karma < 10:
            node.karma += 1
            node.save()
    elif code == 'BAD_MANIFEST':
        node.karma -= 2
        node.save()
    elif code == 'NOT_PUBLISHED':
        node.karma -= 1
        node.save()


def publish_manifest():
    #publish the best most recent posts
    posts = Post.objects.order_by('-received_timestamp')
    posts = posts.filter(karma__gte=-100, is_pinned=True)
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
    our_id = client.id()['ID']
    logging.info('writing manifest to: %s' % our_id)
    with tempfile.TemporaryDirectory() as tmpdirname:
        mani_path = os.path.join(tmpdirname, 'manifest.mp')
        open(mani_path, 'wb').write(raw_mani)
        add_result = store_filepath(mani_path)
    ipfs_path = add_result['Path']
    try:
        client.name_publish(ipfs_path, lifetime="1h")
    except ErrorResponse as error:
        log_fail(error)


def mail_route():
    put_advertisement()
    publish_manifest()
    drive_route()
    explore_new_routes()
    trucking_pool.waitall()
