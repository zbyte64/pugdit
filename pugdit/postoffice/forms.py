from django import forms
from nacl.signing import VerifyKey
from base64 import b64encode, b64decode
from .models import Post, Identity


class PostMarkForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['signature', 'signer']

    def clean(self):
        cleaned_data = super(PostMarkForm, self).clean()
        signer = cleaned_data['signer']
        raw_signature = b64decode(cleaned_data['signature'].encode('utf8'))
        try:
            message = signer.verify(raw_signature)
            cleaned_data['to'], cleaned_data['link'] = message
        except ValueError as error:
            raise forms.ValidationError(str(error))
        return cleaned_data

    def save(self):
        post = super(PostMarkForm, self).save(commit=False)
        post.to = self.cleaned_data['to']
        post.link = self.cleaned_data['link']
        post.save()
        return post


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
        public_key = b64decode(cleaned_data['public_key'].encode('utf8'))
        signed_username = b64decode(cleaned_data['signed_username'].encode('utf8'))
        try:
            vk = VerifyKey(public_key)
            username = vk.verify(signed_username)
        except ValueError as error:
            print('validation fail:', error)
            raise forms.ValidationError(str(error))
        except Exception as error:
            print(error)
            print(type(error))
            raise forms.ValidationError(str(error))
        else:
            if username != self.owner.username.encode('utf8'):
                raise forms.ValidationError('Signature was not authorized for this user')
        print('verified')
        return cleaned_data

    def save(self):
        identity = super(RegisterIdentityForm, self).save(commit=False)
        identity.owner = self.owner
        identity.save()
        return identity
