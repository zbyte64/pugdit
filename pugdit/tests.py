from snapshottest.django import TestCase
#from graphene.test import Client
from django.contrib.auth.models import User
from django.test import Client


client = Client()

REGISTER_IDENTITY_SAMPLE = '''
{"operationName":"registerIdentity","variables":{"signedUsername":"/emDLfHcZCxuu0wUBCbhXapBg3DKLTSjcQtSvJzJ0TLHIBfm28LhunLrm1PXJUWa4UQmaN8dH11qghcM4SdWC2FkbWlu","publicKey":"+mVYLVA8J3NcXDj/366os5MaIvjLJH5ujXBb/kUl/GM="},"query":"mutation registerIdentity($signedUsername: String!, $publicKey: String!) {\n  registerIdentity(input: {signedUsername: $signedUsername, publicKey: $publicKey}) {\n    identity {\n      id\n      publicKey\n      karma\n      __typename\n    }\n    __typename\n  }\n}\n"}
'''

class APITestCase(TestCase):
    def test_api_index(self):
        """Testing the API for /graphql/"""
        self.user = User.objects.create_user(username='admin', password='12345')
        login = self.client.login(username='admin')#, password='12345')
        self.assertMatchSnapshot(login)#, name='login')
        my_api_response = client.get('/graphql/')
        self.assertMatchSnapshot(my_api_response)#, name='graphql index')

        ident_response = client.post('/graphql/', REGISTER_IDENTITY_SAMPLE, content_type='application/json')
        self.assertMatchSnapshot(ident_response)#, name='register identity')
