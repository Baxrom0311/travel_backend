from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'country', 'rating', 'title', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at']


class ReviewCreateSerializer(serializers.ModelSerializer):
    target_type = serializers.ChoiceField(
        choices=['hotel', 'attraction', 'restaurant', 'tour'],
        write_only=True
    )
    target_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Review
        fields = ['name', 'email', 'country', 'rating', 'title', 'comment', 'target_type', 'target_id']

    def validate_rating(self, v):
        if v < 1 or v > 5:
            raise serializers.ValidationError("Reyting 1 dan 5 gacha bo'lishi kerak")
        return v

    def validate_comment(self, v):
        if len(v.strip()) < 10:
            raise serializers.ValidationError("Fikr kamida 10 ta belgi")
        return v.strip()

    def create(self, validated_data):
        target_type = validated_data.pop('target_type')
        target_id = validated_data.pop('target_id')

        model_map = {
            'hotel': ('hotels', 'hotel'),
            'attraction': ('attractions', 'attraction'),
            'restaurant': ('restaurants', 'restaurant'),
            'tour': ('tours', 'tour'),
        }
        app_label, model_name = model_map[target_type]
        ct = ContentType.objects.get(app_label=app_label, model=model_name)

        return Review.objects.create(
            content_type=ct,
            object_id=target_id,
            **validated_data
        )
