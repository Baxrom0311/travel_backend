"""Cache-Control header mixin for public list endpoints."""
from django.utils.cache import patch_cache_control


class PublicCacheMixin:
    """Adds Cache-Control: public, max-age=300 to GET responses."""
    cache_max_age = 300

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        if request.method == 'GET' and response.status_code == 200:
            patch_cache_control(response, public=True, max_age=self.cache_max_age)
        return response
