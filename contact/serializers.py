from rest_framework import serializers
from hotels.models import ContactMessage


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'message']

    def validate_name(self, v):
        if len(v.strip()) < 2:
            raise serializers.ValidationError("Ism kamida 2 ta belgi bo'lishi kerak.")
        return v.strip()

    def validate_message(self, v):
        if len(v.strip()) < 10:
            raise serializers.ValidationError("Xabar kamida 10 ta belgi bo'lishi kerak.")
        return v.strip()
