from django.urls import path

from .views import CreateUrlView, EditUrlView, UrlRedirectView


urlpatterns = [
    path("", CreateUrlView.as_view(), name="home_page"),
    path("edit/", EditUrlView.as_view(), name="edit_page"),
    path("<slug:hashed_url>/", UrlRedirectView.as_view(), name="url_redirecter")
]
