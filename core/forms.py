from django import forms


class UrlForm(forms.Form):
    # TODO (future improvement): validate url input further
    ## deal with "https://" or "http://" accordingly, remove trailing slashes, empty url query, etc
    url = forms.URLField(required=True, max_length=255)
    hashed_url = forms.CharField(required=False, max_length=255)
