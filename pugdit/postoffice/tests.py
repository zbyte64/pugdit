from django.test import TestCase
from .mailtruck import parse_manifest, mail_route
import umsgpack


TEST_MANIFEST_FIXTURE = {
    'identities': ['bvHKiFuCjQL0SIyqfjLmOKoA+Ovy3NZrgs0HPOeY8M4='],
    'posts': [['lnXfEhnrr/ZsmhJ37BmnH/PoLTYFUd+NFB9EiDMgr9zrM0Nl8+vJep3GYY3sl762kYYPZeiRUVvKYUiS+iBMD5LZMmhlbGxvL29xQkVKNlN6TFJvSGpGa1FBb200cHRET2hOR0RyT2pURkh2N2FDbVNNOTQ92TkvaXBmcy9RbVU3dVVaYXB4NE1rY2dkbzhFVGpBSG1rbWc0OWhBR05ubWRYRmtNMzZKdnVaL3Bvc3Q=', 0]]
}


class DeliveryTestCase(TestCase):
    def test_parse_manifest(self):
        payload = umsgpack.packb(TEST_MANIFEST_FIXTURE)
        mani = parse_manifest(payload)

    def test_mail_route(self):
        mail_route()
