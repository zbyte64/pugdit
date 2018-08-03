from django import forms
from nacl.signing import VerifyKey
from .models import Post
from .mailtruck import check_signature


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
