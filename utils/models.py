from urllib.parse import urlparse, urlunparse

from django.conf import settings
from django.db import models


def upload_to(instance, filename):
    return "%s/%s" % (instance._meta.app_label, filename)


class UrlMixin(models.Model):
    """
    A replacement for get_absolute_url(). Models extending this mixin should have either get_url or get_url_path implemented
    """

    class Meta:
        abstract = True

    def get_url(self):
        if hasattr(self.get_url_path, "dont_recurse"):
            raise NotImplementedError
        try:
            path = self.get_url_path()
        except NotImplementedError:
            raise
        website_url = getattr(
            settings, "DEFAULT_WEBSITE_URL", "http://127.0.0.1:8000"
        )
        return website_url + path

    get_url.dont_recurse = True

    def get_url_path(self):
        if hasattr(self.get_url, "dont_recurse"):
            raise NotImplementedError
        try:
            url = self.get_url()
        except NotImplementedError:
            raise

        bits = urlparse(url)
        return urlunparse(("", "") + bits[2:])

    get_url_path.dont_recurse = True

    def get_absolute_url(self):
        return self.get_url_path()
