from rest_framework import serializers
from .models import Testimonial


class TestimonialSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Testimonial
        fields = [
            'id', 'name', 'country', 'role', 'rating',
            'text_uz', 'text_en', 'text_ru',
            'avatar_url', 'is_featured', 'order',
        ]
    
    def get_avatar_url(self, obj) -> str | None:
        if obj.avatar:
            try:
                return obj.avatar.url
            except Exception:
                return None
        return None
