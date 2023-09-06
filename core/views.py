from django.shortcuts import render, redirect
from django.views import View

from core.models import Url
from core.forms import CreateUrlForm, EditUrlForm
from core.generators import generate_pin_and_hash, convert_pin_to_hash


class CreateUrlView(View):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = CreateUrlForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form})

        url = form.cleaned_data.get("url")
        hashed_url = form.cleaned_data.get("hashed_url")

        # check for existing hashed_url (FEATURE 2)
        if hashed_url and Url.objects.filter(hashed_url=hashed_url).exists():
            form.add_error("hashed_url", "Sorry! That specified hash is already being used! Remove custom hash or enter a different one")
            return render(request, self.template_name, {"form": form})

        # TODO (future feature): return the existing hashed_url if one already points to the given url

        # Pin Creation (BONUS FEATURE)
        pincode, pincode_hash = generate_pin_and_hash()
        obj = Url.objects.create(url=url, hashed_url=hashed_url, hashed_pin=pincode_hash)

        return render(
            request, self.template_name, {"short_url": obj.get_full_short_url(), "pin": pincode}
        )

class EditUrlView(View):
    template_name = "edit.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = EditUrlForm(request.POST)
        pin_checked = form.data.get("pincheck")
        short_url_or_hash = form.data.get("short_url")

        if not form.is_valid():
            return render(
                request,
                self.template_name,
                {"form": form, "pin_ok": pin_checked, "short_url": short_url_or_hash}
            )

        pin = form.cleaned_data.get("pin")
        url = form.cleaned_data.get("url")

        # get object with given hashed_url
        try:
            hashed_url = short_url_or_hash.replace("http://localhost:8000/", "")
            obj = Url.objects.get(hashed_url=hashed_url) # will raise NotFound exception
        except:
            form.add_error("short_url", "The given short url/hash has not been claimed")
            return render(
                request,
                self.template_name,
                {"form": form, "pin_ok": pin_checked, "short_url": short_url_or_hash}
            )

        # handle pin submission
        if not pin_checked:
            # check if the correct pin was entered
            hashed_pin = convert_pin_to_hash(pin)
            if hashed_pin != obj.hashed_pin:
                form.add_error("pin", "PIN is incorrect")
                return render(
                    request,
                    self.template_name,
                    {"form": form, "pin_ok": False, "short_url": short_url_or_hash}
                )

            return render(
                request,
                self.template_name,
                {"form": form, "pin_ok": True, "short_url": obj.get_full_short_url(), "url": obj.url}
            )

        # handle saving new url
        else:
            obj.url = url
            obj.save()
        
            return render(
                request,
                self.template_name,
                {"form": form, "pin_ok": True, "short_url": obj.get_full_short_url(), "url": url}
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
