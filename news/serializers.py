from rest_framework import serializers
from .models import News, NewsImage


class NewsImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = NewsImage
        fields = ['id', 'image_url', 'caption', 'order']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url


class NewsListSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    excerpt = serializers.SerializerMethodField()
    cover_image_url = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = [
            'id', 'title', 'slug', 'excerpt', 'cover_image_url',
            'author', 'published_at', 'is_featured',
        ]

    def _lang(self):
        return self.context.get('lang', 'uz')

    def get_title(self, obj):
        lang = self._lang()
        return getattr(obj, f'title_{lang}', '') or obj.title_uz

    def get_excerpt(self, obj):
        lang = self._lang()
        return getattr(obj, f'excerpt_{lang}', '') or obj.excerpt_uz

    def get_cover_image_url(self, obj):
        if obj.cover_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.cover_image.url)
            return obj.cover_image.url
        return None


class NewsDetailSerializer(NewsListSerializer):
    content = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta(NewsListSerializer.Meta):
        fields = NewsListSerializer.Meta.fields + [
            'content', 'images',
            'title_uz', 'title_en', 'title_ru',
            'content_uz', 'content_en', 'content_ru',
        ]

    def get_content(self, obj):
        lang = self._lang()
        return getattr(obj, f'content_{lang}', '') or obj.content_uz

    def get_images(self, obj):
        return NewsImageSerializer(obj.images.all(), many=True, context=self.context).data
