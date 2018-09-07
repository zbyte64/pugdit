# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['APITestCase::test_register_identity 1'] = {
    'data': {
        'registerIdentity': {
            '__typename': 'RegisterIdentityMutationPayload',
            'identity': {
                '__typename': 'IdentityNode',
                'id': 'SWRlbnRpdHlOb2RlOjI=',
                'karma': 0,
                'publicKey': '+mVYLVA8J3NcXDj/366os5MaIvjLJH5ujXBb/kUl/GM='
            }
        }
    }
}

snapshots['APITestCase::test_register_identity 2'] = {
    'data': {
        'postMark': {
            '__typename': 'PostMarkMutationPayload',
            'post': {
                '__typename': 'PostNode',
                'id': 'UG9zdE5vZGU6Mg==',
                'link': '/ipfs/Qmf412jQZiuVUtdgnB36FXFX7xg5V6KEbSJ4dpQuhkLyfD',
                'signature': 'oqBEJ6SzLRoHjFkQAom4ptDOhNGDrOjTFHv7aCmSM94YJLvjGjw6DYm0rFxdAzwp21YUCWvAahJWXsY8H0x4DJKlaGVsbG/ZNC9pcGZzL1FtZjQxMmpRWml1VlV0ZGduQjM2RlhGWDd4ZzVWNktFYlNKNGRwUXVoa0x5ZkQ=',
                'signer': {
                    '__typename': 'IdentityNode',
                    'id': 'SWRlbnRpdHlOb2RlOjI='
                },
                'to': 'hello'
            }
        }
    }
}
