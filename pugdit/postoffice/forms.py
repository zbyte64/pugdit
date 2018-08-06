from django import forms
from nacl.signing import VerifyKey
from nacl.encoding import HexEncoder as KeyEncoder
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
        assert self.owner
        cleaned_data = super(RegisterIdentityForm, self).clean()
        vk = VerifyKey(cleaned_data['public_key'], KeyEncoder)
        try:
            vk.verify(self.owner.username, cleaned_data['signed_username'])
        except ValueError as error:
            raise forms.ValidationError(str(error))
        return cleaned_data

    def save(self):
        identity = super(RegisterIdentityForm, self).save(commit=False)
        identity.owner = self.owner
        identity.fingerprint = make_fingerprint(identity.public_key)
        identity.save()
        return identity
