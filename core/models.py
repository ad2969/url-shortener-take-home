import secrets

from django.db import models


class Url(models.Model):
    url = models.URLField(max_length=255)
    hashed_url = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.pk} - {self.url} - {self.hashed_url}"

    def save(self, *args, **kwargs):
        if not self.hashed_url:
            self.hashed_url = self.get_unique_hash()
        super().save(*args, **kwargs)

    # since the hashing function is not actually dependent on the given destination url
    # use this function to ensure that a unique hash is obtained
    def get_unique_hash(self):
        new_hash = self.hash_url()
        # repeat "hash_url" function until a unique hash is obtained
        while Url.objects.filter(hashed_url=new_hash).exists():
           new_hash = self.hash_url()

        return new_hash

    def hash_url(self):
        token = secrets.token_urlsafe(16)[:10]
        return token

    def get_full_short_url(self):
        return f"http://localhost:8000/{self.hashed_url}"
