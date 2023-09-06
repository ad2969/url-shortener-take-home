from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator

class CreateUrlForm(forms.Form):
    # TODO (future improvement): validate url input further
    ## deal with "https://" or "http://" accordingly, remove trailing slashes, empty url query, etc
    url = forms.URLField(required=True, max_length=255)
    hashed_url = forms.CharField(required=False, max_length=255)

class EditUrlForm(forms.Form):
    short_url = forms.CharField(required=True, max_length=255)
    pin = forms.IntegerField(required=True, validators=[
        MaxValueValidator(9999),
        MinValueValidator(0)
    ])

    # hacky way of maintaining "state" - whether PIN has been submitted & checked
    # TODO: better state management
    pincheck = forms.BooleanField(required=False)

    url = forms.URLField(required=False, max_length=255)

    def clean(self):
        cleaned_data = super(EditUrlForm, self).clean()
        is_pin_checked = cleaned_data.get("pincheck")
        url = cleaned_data.get("url")
        # url is required conditional on if pin has already been checked
        if is_pin_checked and not url:
            self.add_error('url', 'Enter a valid URL')
        return cleaned_data
