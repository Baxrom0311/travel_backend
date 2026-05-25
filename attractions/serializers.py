from rest_framework import serializers
from .models import Attraction, AttractionImage


class AttractionImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    caption = serializers.SerializerMethodField()

    class Meta:
        model = AttractionImage
        fields = ['id', 'image_url', 'caption', 'is_cover', 'order']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url

    def get_caption(self, obj):
        lang = self.context.get('lang', 'uz')
        return getattr(obj, f'caption_{lang}', '') or obj.caption_uz


class AttractionListSerializer(serializers.ModelSerializer):
    """Ro'yxat uchun qisqa serializer"""
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    cover_image = serializers.SerializerMethodField()

    class Meta:
        model = Attraction
        fields = [
            'id', 'icon', 'name', 'description', 'cover_image',
            'latitude', 'longitude', 'is_featured', 'order',
        ]

    def _lang(self):
        return self.context.get('lang', 'uz')

    def get_name(self, obj):
        lang = self._lang()
        return getattr(obj, f'name_{lang}', '') or obj.name_uz

    def get_description(self, obj):
        lang = self._lang()
        return getattr(obj, f'description_{lang}', '') or obj.description_uz

    def get_cover_image(self, obj):
        request = self.context.get('request')
        imgs = obj.images.all()
        cover = next((i for i in imgs if i.is_cover), None)
        img = cover or (imgs[0] if imgs else None)
        if img and img.image and request:
            return request.build_absolute_uri(img.image.url)
        return None


class AttractionDetailSerializer(serializers.ModelSerializer):
    """Detail uchun to'liq serializer"""
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    history = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    cover_image = serializers.SerializerMethodField()

    class Meta:
        model = Attraction
        fields = [
            'id', 'icon', 'name', 'description', 'history',
            'name_uz', 'name_en', 'name_ru',
            'description_uz', 'description_en', 'description_ru',
            'video_url', 'cover_image', 'images',
            'latitude', 'longitude',
            'working_hours', 'entrance_fee',
            'is_featured', 'order',
        ]

    def _lang(self):
        return self.context.get('lang', 'uz')

    def get_name(self, obj):
        lang = self._lang()
        return getattr(obj, f'name_{lang}', '') or obj.name_uz

    def get_description(self, obj):
        lang = self._lang()
        return getattr(obj, f'description_{lang}', '') or obj.description_uz

    def get_history(self, obj):
        lang = self._lang()
        return getattr(obj, f'history_{lang}', '') or obj.history_uz

    def get_cover_image(self, obj):
        request = self.context.get('request')
        imgs = obj.images.all()
        cover = next((i for i in imgs if i.is_cover), None)
        img = cover or (imgs[0] if imgs else None)
        if img and img.image and request:
            return request.build_absolute_uri(img.image.url)
        return None

    def get_images(self, obj):
        return AttractionImageSerializer(
            obj.images.all(), many=True, context=self.context
        ).data


# Backward compatibility
AttractionSerializer = AttractionListSerializer
