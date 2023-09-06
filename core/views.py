from django.shortcuts import render, redirect
from django.views import View

from core.models import Url
from core.forms import UrlForm


class HomeView(View):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = UrlForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form})

        url = form.cleaned_data.get("url")
        hashed_url = form.cleaned_data.get("hashed_url")

        # check for existing hashed_url (FEATURE 2)
        if hashed_url and Url.objects.filter(hashed_url=hashed_url).exists():
            form.add_error("hashed_url", "Sorry! That specified hash is already being used! Remove custom hash or enter a different one")
            return render(request, self.template_name, {"form": form})

        # TODO (future feature): return the existing hashed_url if one already points to the given url

        obj = Url.objects.create(url=url, hashed_url=hashed_url)

        return render(
            request, self.template_name, {"short_url": obj.get_full_short_url()}
        )

# URL Redirecter (FEATURE 1)
class UrlRedirectView(View):
    # Alternatively, instead of having the custom "redirect.html" redirect and "404.html" page,
    # we can use the Django-provided Redirect View
    # https://docs.djangoproject.com/en/4.2/ref/class-based-views/base/#redirectview
    template_404 = "404.html"
    template_redirect = "redirect.html"

    def get(self, request, *args, **kwargs):
        try:
            if not "hashed_url" in kwargs: raise Exception()
            hashed_url = kwargs["hashed_url"]
            destination = Url.objects.get(hashed_url=hashed_url) # will raise NotFound exception if row doesn't exist

            # return redirect(destination.url) -- default behaviour, before improvement and adding "redirect.html"
            return render(request, self.template_redirect, context={"url": destination.url})
        except:
            return render(request, self.template_404)
