from rest_framework import serializers
from .models import Event, EventImage


class EventImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = EventImage
        fields = ['id', 'image_url', 'order']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url


class EventListSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    cover_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'cover_image_url',
            'start_date', 'end_date', 'start_time',
            'location', 'is_free', 'price', 'is_featured',
        ]

    def _lang(self):
        return self.context.get('lang', 'uz')

    def get_title(self, obj):
        lang = self._lang()
        return getattr(obj, f'title_{lang}', '') or obj.title_uz

    def get_description(self, obj):
        lang = self._lang()
        return getattr(obj, f'description_{lang}', '') or obj.description_uz

    def get_location(self, obj):
        lang = self._lang()
        return getattr(obj, f'location_{lang}', '') or obj.location_uz

    def get_cover_image_url(self, obj):
        if obj.cover_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.cover_image.url)
            return obj.cover_image.url
        return None


class EventDetailSerializer(EventListSerializer):
    images = serializers.SerializerMethodField()

    class Meta(EventListSerializer.Meta):
        fields = EventListSerializer.Meta.fields + [
            'latitude', 'longitude', 'images',
            'title_uz', 'title_en', 'title_ru',
            'description_uz', 'description_en', 'description_ru',
        ]

    def get_images(self, obj):
        return EventImageSerializer(obj.images.all(), many=True, context=self.context).data
