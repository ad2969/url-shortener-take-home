from django.db import models
from core.generators import generate_hash_url


class Url(models.Model):
    url = models.URLField(max_length=255)
    hashed_url = models.CharField(max_length=10, unique=True, db_index=True)
    hashed_pin = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.pk} - {self.url} - {self.hashed_url}"

    def save(self, *args, **kwargs):
        if not self.hashed_url:
            self.hashed_url = self.get_unique_hash()
        super().save(*args, **kwargs)

    # since the hashing function is not actually dependent on the given destination url
    # use this function to ensure that a unique hash is obtained
    def get_unique_hash(self):
        new_hash = generate_hash_url()
        # repeat "generate_hash_url" function until a unique hash is obtained
        while Url.objects.filter(hashed_url=new_hash).exists():
           new_hash = generate_hash_url()

        return new_hash

    def get_full_short_url(self):
        return f"http://localhost:8000/{self.hashed_url}"
