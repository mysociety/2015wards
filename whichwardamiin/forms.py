from django import forms

from mapit.utils import is_valid_postcode
from mapit import countries
from mapit.models import Postcode


class PostcodeForm(forms.Form):
    """Simple form class for a postcode lookup form"""

    postcode = forms.CharField(required=True)

    def clean_postcode(self):
        postcode = self.cleaned_data['postcode']
        if not is_valid_postcode(postcode):
            raise forms.ValidationError("Postcode doesn't seem to be valid")
        if hasattr(countries, 'canonical_postcode'):
            postcode = countries.canonical_postcode(postcode)
        try:
            postcode = Postcode.objects.get(postcode=postcode)
        except Postcode.DoesNotExist:
            raise forms.ValidationError("Postcode could not be found")

        return postcode
