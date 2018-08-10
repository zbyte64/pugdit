from snapshottest.django import TestCase
from graphene.test import Client
from .postoffice.schema import schema
from django.test import RequestFactory
from django.contrib.auth.models import User

client = Client(schema)


REGISTER_IDENTITY_SAMPLE = {
    "variables":{"signedUsername":"/emDLfHcZCxuu0wUBCbhXapBg3DKLTSjcQtSvJzJ0TLHIBfm28LhunLrm1PXJUWa4UQmaN8dH11qghcM4SdWC2FkbWlu","publicKey":"+mVYLVA8J3NcXDj/366os5MaIvjLJH5ujXBb/kUl/GM="},
    "query":"mutation registerIdentity($signedUsername: String!, $publicKey: String!) {\n  registerIdentity(input: {signedUsername: $signedUsername, publicKey: $publicKey}) {\n    identity {\n      id\n      publicKey\n      karma\n      __typename\n    }\n    __typename\n  }}"
}

class APITestCase(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.user = User.objects.create_user(username='admin', password='12345')
        self.factory = RequestFactory()
        context = self.factory.generic('POST', '/graphql/', content_type='application/json')
        context.user = self.user
        self.context = context

    def test_register_identity(self):
        """Register an identity for an existing user"""
        ident_response = client.execute(REGISTER_IDENTITY_SAMPLE['query'], variable_values=REGISTER_IDENTITY_SAMPLE['variables'], context_value=self.context)
        self.assertMatchSnapshot(ident_response)
