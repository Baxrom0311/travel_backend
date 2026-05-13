from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import SiteSettings
from .serializers import SiteSettingsSerializer, MAP_PROVIDERS_CONFIG


@api_view(['GET'])
def get_site_settings(request):
    """GET /api/settings/ — sayt sozlamalari (public)."""
    settings = SiteSettings.get()
    serializer = SiteSettingsSerializer(settings)
    return Response(serializer.data)


@api_view(['GET'])
def get_map_providers(request):
    """GET /api/settings/map-providers/ — barcha xarita provayderlari."""
    return Response({
        'providers': [
            {'key': k, **v}
            for k, v in MAP_PROVIDERS_CONFIG.items()
        ]
    })
