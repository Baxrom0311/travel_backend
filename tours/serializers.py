from rest_framework import serializers
from .models import Tour, TourImage


class TourImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = TourImage
        fields = ['id', 'image_url', 'caption', 'order']

    def get_image_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.image.url) if request else obj.image.url


class TourListSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()
    cover_image_url = serializers.SerializerMethodField()
    difficulty_label = serializers.CharField(source='get_difficulty_display', read_only=True)
    duration_type_label = serializers.CharField(source='get_duration_type_display', read_only=True)

    class Meta:
        model = Tour
        fields = [
            'id', 'slug', 'title', 'short_description', 'cover_image_url',
            'price', 'duration', 'duration_type', 'duration_type_label',
            'difficulty', 'difficulty_label', 'rating',
            'max_people', 'min_people', 'is_featured',
        ]

    def _lang(self):
        return self.context.get('lang', 'uz')

    def get_title(self, obj):
        return getattr(obj, f'title_{self._lang()}', '') or obj.title_uz

    def get_short_description(self, obj):
        return getattr(obj, f'short_description_{self._lang()}', '') or obj.short_description_uz

    def get_cover_image_url(self, obj):
        if obj.cover_image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.cover_image.url) if request else obj.cover_image.url
        return None


class TourDetailSerializer(TourListSerializer):
    description = serializers.SerializerMethodField()
    itinerary = serializers.SerializerMethodField()
    includes = serializers.SerializerMethodField()
    excludes = serializers.SerializerMethodField()
    meeting_point = serializers.SerializerMethodField()
    images = TourImageSerializer(many=True, read_only=True)

    class Meta(TourListSerializer.Meta):
        fields = TourListSerializer.Meta.fields + [
            'description', 'itinerary', 'includes', 'excludes',
            'meeting_point', 'guide_languages', 'images',
        ]

    def get_description(self, obj):
        return getattr(obj, f'description_{self._lang()}', '') or obj.description_uz

    def get_itinerary(self, obj):
        return getattr(obj, f'itinerary_{self._lang()}', '') or obj.itinerary_uz

    def get_includes(self, obj):
        return getattr(obj, f'includes_{self._lang()}', '') or obj.includes_uz

    def get_excludes(self, obj):
        return getattr(obj, f'excludes_{self._lang()}', '') or obj.excludes_uz

    def get_meeting_point(self, obj):
        return getattr(obj, f'meeting_point_{self._lang()}', '') or obj.meeting_point_uz
