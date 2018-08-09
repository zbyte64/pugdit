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
    public_key = forms.CharField(max_length=77)
    signed_username = forms.CharField()

    class Meta:
        model = Identity
        fields = []
        exclude = ['public_key']

    def __init__(self, data=None, owner=None):
        super(RegisterIdentityForm, self).__init__(data=data)
        self.owner = owner

    def clean_public_key(self):
        data = self.cleaned_data['public_key']
        self.cleaned_data['public_key_base64'] = data
        return b64decode(data.encode('utf8'))

    def clean_signed_username(self):
        data = self.cleaned_data['signed_username']
        return b64decode(data.encode('utf8'))

    def clean(self):
        print('clean', self._errors)
        assert self.owner
        cleaned_data = super(RegisterIdentityForm, self).clean()
        print(cleaned_data, self.owner.username)
        public_key = cleaned_data['public_key']
        signed_username = cleaned_data['signed_username']
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
        print('verified', cleaned_data)
        return cleaned_data

    def save(self):
        identity = super(RegisterIdentityForm, self).save(commit=False)
        identity.owner = self.owner
        identity.public_key = self.cleaned_data['public_key_base64']
        identity.save()
        return identity
