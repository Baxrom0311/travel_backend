from rest_framework import serializers
from .models import TransportRoute


class TransportRouteSerializer(serializers.ModelSerializer):
    """
    ?lang=uz|en|ru → 'name', 'from_location', 'to_location',
                       'badge', 'description' tanlangan tilda qaytadi.
    Barcha til variantlari ham mavjud.
    """
    type_label      = serializers.CharField(source='get_transport_type_display', read_only=True)
    duration_label  = serializers.SerializerMethodField()
    price_label     = serializers.SerializerMethodField()

    # Ko'p tillilik — tanlangan tilda
    from_location   = serializers.SerializerMethodField()
    to_location     = serializers.SerializerMethodField()
    badge           = serializers.SerializerMethodField()
    description     = serializers.SerializerMethodField()

    class Meta:
        model  = TransportRoute
        fields = [
            'id', 'transport_type', 'type_label', 'icon',
            # Ko'p tillilik — tanlangan tilda
            'from_location', 'to_location', 'badge', 'description',
            # Barcha til variantlari
            'from_location_uz', 'from_location_en', 'from_location_ru',
            'to_location_uz',   'to_location_en',   'to_location_ru',
            'badge_uz', 'badge_en', 'badge_ru',
            'description_uz', 'description_en', 'description_ru',
            # Narx va vaqt
            'duration_min', 'duration_max', 'duration_label',
            'price_min', 'price_max', 'price_label',
            # Badge uslubi
            'badge_style',
            'order',
        ]

    def _lang(self):
        return self.context.get('lang', 'uz')

    def get_from_location(self, obj) -> str:
        lang = self._lang()
        return getattr(obj, f'from_location_{lang}', '') or obj.from_location_uz

    def get_to_location(self, obj) -> str:
        lang = self._lang()
        return getattr(obj, f'to_location_{lang}', '') or obj.to_location_uz

    def get_badge(self, obj) -> str:
        lang = self._lang()
        return getattr(obj, f'badge_{lang}', '') or obj.badge_uz

    def get_description(self, obj) -> str:
        lang = self._lang()
        return getattr(obj, f'description_{lang}', '') or obj.description_uz

    def get_duration_label(self, obj) -> str:
        if obj.duration_min == obj.duration_max:
            return f"{obj.duration_min} daqiqa"
        return f"{obj.duration_min}–{obj.duration_max} daqiqa"

    def get_price_label(self, obj) -> str:
        if obj.price_min == obj.price_max:
            return f"~{obj.price_min:,} UZS"
        return f"{obj.price_min:,} – {obj.price_max:,} UZS"


class TransportFilterSerializer(serializers.Serializer):
    type = serializers.ChoiceField(
        choices=TransportRoute.TYPE_CHOICES,
        required=False,
        help_text="taxi | bus | train",
    )
