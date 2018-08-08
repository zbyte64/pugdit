from django import forms
from nacl.signing import VerifyKey
from nacl.encoding import Base64Encoder as KeyEncoder
from base64 import b64encode, b64decode
from .models import Post, Identity
from .mailtruck import check_signature, make_fingerprint


class PostMarkForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['to', 'link', 'timestamp', 'signature', 'signer']

    def clean(self):
        cleaned_data = super(PostMarkForm, self).clean()
        public_key = cleaned_data['signer'].public_key
        vk = VerifyKey(public_key, KeyEncoder)
        try:
            check_signature(env, vk)
        except ValueError as error:
            raise forms.ValidationError(str(error))
        return cleaned_data


class RegisterIdentityForm(forms.ModelForm):
    signed_username = forms.CharField()

    class Meta:
        model = Identity
        fields = ['public_key']

    def __init__(self, data=None, owner=None):
        super(RegisterIdentityForm, self).__init__(data=data)
        self.owner = owner

    def clean(self):
        print('clean')
        assert self.owner
        cleaned_data = super(RegisterIdentityForm, self).clean()
        print(cleaned_data, self.owner.username)
        public_key = cleaned_data['public_key'].encode('utf8')
        #signing was against native-encoding
        signed_username = b64decode(cleaned_data['signed_username'].encode('utf8'))
        username = self.owner.username.encode('utf8')
        try:
            vk = VerifyKey(public_key, KeyEncoder)
            vk.verify(username, signed_username)
        except ValueError as error:
            print('validation fail:', error)
            raise forms.ValidationError(str(error))
        except Exception as error:
            print(error)
            print(type(error))
            raise forms.ValidationError(str(error))
        print('verified')
        return cleaned_data

    def save(self):
        identity = super(RegisterIdentityForm, self).save(commit=False)
        identity.owner = self.owner
        identity.fingerprint = make_fingerprint(identity.public_key)
        identity.save()
        return identity
