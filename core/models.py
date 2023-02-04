from django.db import models
from urllib.parse import unquote
# Create your models here.

class UnicodeUrl(models.Model):
    class Meta:
        abstract = True

    def get_unicode_url(self):
        url = self.get_absolute_url()
        return unquote(url)