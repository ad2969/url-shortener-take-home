from django.urls import path

from .views import HomeView, UrlRedirectView


urlpatterns = [
    path("", HomeView.as_view(), name="home_page"),
    path("<slug:hashed_url>/", UrlRedirectView.as_view(), name="url_redirecter")
]
