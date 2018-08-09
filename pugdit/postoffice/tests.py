from django.test import TestCase
from .mailtruck import parse_manifest, mail_route
import umsgpack


class DeliveryTestCase(TestCase):
    def test_parse_manifest(self):
        payload = umsgpack.packb({
            'posts': [],
            'identities': [],
        })
        mani = parse_manifest(payload)

    def test_mail_route(self):
        mail_route()
