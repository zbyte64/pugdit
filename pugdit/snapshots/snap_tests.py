# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['APITestCase::test_api_index 1'] = {
    'data': {
        'registerIdentity': {
            '__typename': 'RegisterIdentityMutationPayload',
            'identity': {
                '__typename': 'IdentityNode',
                'id': 'SWRlbnRpdHlOb2RlOjE=',
                'karma': 0,
                'publicKey': '+mVYLVA8J3NcXDj/366os5MaIvjLJH5ujXBb/kUl/GM='
            }
        }
    }
}

snapshots['APITestCase::test_register_identity 1'] = {
    'data': {
        'registerIdentity': {
            '__typename': 'RegisterIdentityMutationPayload',
            'identity': {
                '__typename': 'IdentityNode',
                'id': 'SWRlbnRpdHlOb2RlOjE=',
                'karma': 0,
                'publicKey': '+mVYLVA8J3NcXDj/366os5MaIvjLJH5ujXBb/kUl/GM='
            }
        }
    }
}
