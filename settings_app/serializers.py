from rest_framework import serializers
from .models import SiteSettings, MAP_PROVIDERS


# Map tile URLs and attributions
MAP_PROVIDERS_CONFIG = {
    'osm': {
        'name': 'OpenStreetMap',
        'url': 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        'attribution': '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        'max_zoom': 19,
    },
    'carto_voyager': {
        'name': 'CartoDB Voyager',
        'url': 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png',
        'attribution': '&copy; OpenStreetMap &copy; <a href="https://carto.com/attributions">CARTO</a>',
        'max_zoom': 20,
    },
    'carto_positron': {
        'name': 'CartoDB Positron',
        'url': 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
        'attribution': '&copy; OpenStreetMap &copy; <a href="https://carto.com/attributions">CARTO</a>',
        'max_zoom': 20,
    },
    'carto_dark': {
        'name': 'CartoDB Dark Matter',
        'url': 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
        'attribution': '&copy; OpenStreetMap &copy; <a href="https://carto.com/attributions">CARTO</a>',
        'max_zoom': 20,
    },
    'stadia_alidade': {
        'name': 'Stadia Alidade Smooth',
        'url': 'https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png',
        'attribution': '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a> &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; OpenStreetMap',
        'max_zoom': 20,
    },
    'stadia_outdoors': {
        'name': 'Stadia Outdoors',
        'url': 'https://tiles.stadiamaps.com/tiles/outdoors/{z}/{x}/{y}{r}.png',
        'attribution': '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a> &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; OpenStreetMap',
        'max_zoom': 20,
    },
    'stamen_toner': {
        'name': 'Stamen Toner',
        'url': 'https://tiles.stadiamaps.com/tiles/stamen_toner/{z}/{x}/{y}{r}.png',
        'attribution': '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a> &copy; <a href="https://stamen.com/">Stamen Design</a>',
        'max_zoom': 20,
    },
    'stamen_terrain': {
        'name': 'Stamen Terrain',
        'url': 'https://tiles.stadiamaps.com/tiles/stamen_terrain/{z}/{x}/{y}{r}.png',
        'attribution': '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a> &copy; <a href="https://stamen.com/">Stamen Design</a>',
        'max_zoom': 18,
    },
    'esri_satellite': {
        'name': 'Esri World Imagery',
        'url': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        'attribution': 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
        'max_zoom': 19,
    },
    'esri_streets': {
        'name': 'Esri World Street Map',
        'url': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',
        'attribution': 'Tiles &copy; Esri',
        'max_zoom': 19,
    },
    'opentopo': {
        'name': 'OpenTopoMap',
        'url': 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
        'attribution': 'Map data: &copy; OpenStreetMap &copy; SRTM | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a>',
        'max_zoom': 17,
    },
}


class MapProviderConfigSerializer(serializers.Serializer):
    key = serializers.CharField()
    name = serializers.CharField()
    url = serializers.CharField()
    attribution = serializers.CharField()
    max_zoom = serializers.IntegerField()


class SiteSettingsSerializer(serializers.ModelSerializer):
    map = serializers.SerializerMethodField()
    map_dark = serializers.SerializerMethodField()

    class Meta:
        model = SiteSettings
        fields = [
            'site_name', 'site_tagline', 'site_description',
            'contact_email', 'contact_phone', 'contact_address',
            'facebook_url', 'instagram_url', 'youtube_url', 'telegram_url',
            'maintenance_mode', 'maintenance_message',
            'map_default_zoom',
            'map_provider', 'map_dark_provider',
            'map', 'map_dark',
            'updated_at',
        ]

    def _get_map_config(self, key: str) -> dict:
        config = MAP_PROVIDERS_CONFIG.get(key, MAP_PROVIDERS_CONFIG['osm'])
        return {'key': key, **config}

    def get_map(self, obj) -> dict:
        return self._get_map_config(obj.map_provider)

    def get_map_dark(self, obj) -> dict:
        return self._get_map_config(obj.map_dark_provider)
