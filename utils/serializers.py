"""Base serializer patterns for multi-language support."""
from rest_framework import serializers


class TranslatedFieldMixin:
    """
    Adds translated field support to serializers.
    
    Usage:
        class MySerializer(TranslatedFieldMixin, serializers.ModelSerializer):
            translated_fields = ['name', 'description']
            # Model must have: name_uz, name_en, name_ru
    """
    translated_fields: list[str] = []

    def _get_lang(self) -> str:
        return self.context.get('lang', 'uz')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        lang = self._get_lang()
        for field in self.translated_fields:
            if field in data:
                # Replace `name` with `name_{lang}` value
                value = getattr(instance, f'{field}_{lang}', '') or getattr(instance, f'{field}_uz', '')
                data[field] = value
        return data


class ImageUrlMixin:
    """Returns absolute URL for ImageField."""
    
    def build_image_url(self, image_field) -> str | None:
        if not image_field:
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(image_field.url)
        return image_field.url
