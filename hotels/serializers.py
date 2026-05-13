from rest_framework import serializers
from .models import Hotel, HotelImage, Amenity, ContactMessage


class AmenitySerializer(serializers.ModelSerializer):
    """?lang=uz|en|ru → 'name' field"""
    name = serializers.SerializerMethodField()

    class Meta:
        model = Amenity
        fields = ['id', 'icon', 'name', 'name_uz', 'name_en', 'name_ru']

    def get_name(self, obj) -> str:
        return obj.get_name(self.context.get('lang', 'uz'))


class HotelImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = HotelImage
        fields = ['id', 'image_url', 'is_cover', 'order']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url if obj.image else None


class HotelListSerializer(serializers.ModelSerializer):
    """Mehmonxonalar ro'yxati — qisqa"""
    amenities = AmenitySerializer(many=True, read_only=True)
    cover_image = serializers.SerializerMethodField()
    city_label = serializers.CharField(source='get_city_display', read_only=True)
    stars_label = serializers.SerializerMethodField()

    # Localized (language-dependent)
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    address_i18n = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = [
            'id',
            # Name (localized + all variants)
            'name', 'name_en', 'name_ru',
            # City
            'city', 'city_label',
            # Stars & rating
            'stars', 'stars_label', 'rating',
            # Price
            'price_per_night',
            # Address
            'address_i18n', 'address', 'address_en', 'address_ru',
            # Location
            'latitude', 'longitude',
            # Description
            'description', 'description_uz',
            # Media
            'cover_image',
            # Amenities
            'amenities',
            # Featured
            'is_featured',
        ]

    def _lang(self):
        return self.context.get('lang', 'uz')

    def get_name(self, obj):
        return obj.get_name(self._lang())

    def get_description(self, obj):
        return obj.get_description(self._lang())

    def get_address_i18n(self, obj):
        return obj.get_address(self._lang())

    def get_stars_label(self, obj):
        return '★' * obj.stars + '☆' * (5 - obj.stars)

    def get_cover_image(self, obj):
        request = self.context.get('request')
        img = obj.images.filter(is_cover=True).first() or obj.images.first()
        if img and img.image and request:
            return request.build_absolute_uri(img.image.url)
        return None


class HotelDetailSerializer(HotelListSerializer):
    """Batafsil — barcha rasmlar bilan"""
    images = HotelImageSerializer(many=True, read_only=True)

    class Meta(HotelListSerializer.Meta):
        fields = HotelListSerializer.Meta.fields + ['images', 'description_en', 'description_ru', 'google_maps_url']


class HotelFilterSerializer(serializers.Serializer):
    city = serializers.ChoiceField(choices=Hotel.CITY_CHOICES, required=False)
    featured = serializers.BooleanField(required=False)
    stars = serializers.IntegerField(min_value=1, max_value=5, required=False)
    search = serializers.CharField(max_length=100, trim_whitespace=True, required=False)
    amenity = serializers.IntegerField(min_value=1, required=False)
    min_price = serializers.IntegerField(min_value=0, required=False)
    max_price = serializers.IntegerField(min_value=0, required=False)
    ordering = serializers.ChoiceField(
        choices=['rating', '-rating', 'price_per_night', '-price_per_night', 'stars', '-stars', 'name', '-name'],
        required=False,
    )

    def validate(self, attrs):
        if attrs.get('min_price') and attrs.get('max_price'):
            if attrs['min_price'] > attrs['max_price']:
                raise serializers.ValidationError({'min_price': "Min narx max'dan katta bo'lmasligi kerak."})
        return attrs


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'message']

    def validate_name(self, v):
        if len(v.strip()) < 2:
            raise serializers.ValidationError("Ism kamida 2 ta belgi")
        return v.strip()

    def validate_message(self, v):
        if len(v.strip()) < 10:
            raise serializers.ValidationError("Xabar kamida 10 ta belgi")
        return v.strip()
