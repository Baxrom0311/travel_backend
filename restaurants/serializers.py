from rest_framework import serializers
from .models import Restaurant, RestaurantImage, Cuisine


class CuisineSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Cuisine
        fields = ['id', 'icon', 'name', 'name_uz', 'name_en', 'name_ru']

    def get_name(self, obj):
        lang = self.context.get('lang', 'uz')
        return getattr(obj, f'name_{lang}', '') or obj.name_uz


class RestaurantImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = RestaurantImage
        fields = ['id', 'image_url', 'is_cover', 'order']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url


class RestaurantListSerializer(serializers.ModelSerializer):
    cuisines = CuisineSerializer(many=True, read_only=True)
    cover_image = serializers.SerializerMethodField()
    city_label = serializers.CharField(source='get_city_display', read_only=True)
    description = serializers.SerializerMethodField()
    address_i18n = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = [
            'id', 'name', 'name_en', 'name_ru',
            'description', 'description_uz',
            'cuisines', 'city', 'city_label',
            'price_range', 'rating',
            'address_i18n', 'address',
            'latitude', 'longitude',
            'phone', 'website', 'working_hours',
            'has_wifi', 'has_parking', 'has_outdoor_seating',
            'is_halal', 'is_vegetarian_friendly',
            'cover_image', 'is_featured',
        ]

    def _lang(self):
        return self.context.get('lang', 'uz')

    def get_description(self, obj):
        return getattr(obj, f'description_{self._lang()}', '') or obj.description_uz

    def get_address_i18n(self, obj):
        return getattr(obj, f'address_{self._lang()}', '') or obj.address

    def get_cover_image(self, obj):
        request = self.context.get('request')
        imgs = obj.images.all()
        cover = next((i for i in imgs if i.is_cover), None)
        img = cover or (imgs[0] if imgs else None)
        if img and img.image and request:
            return request.build_absolute_uri(img.image.url)
        return None


class RestaurantDetailSerializer(RestaurantListSerializer):
    images = RestaurantImageSerializer(many=True, read_only=True)

    class Meta(RestaurantListSerializer.Meta):
        fields = RestaurantListSerializer.Meta.fields + [
            'description_en', 'description_ru',
            'address_en', 'address_ru', 'images',
        ]
