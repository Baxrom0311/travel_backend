from django.contrib import admin
from .models import TransportRoute


@admin.register(TransportRoute)
class TransportRouteAdmin(admin.ModelAdmin):
    list_display  = ['icon', 'transport_type', 'price_min', 'price_max', 'duration_min', 'duration_max', 'order']
    list_display_links = ['transport_type']
    list_editable = ['price_min', 'price_max', 'order']
    list_filter   = ['transport_type']
    fieldsets = (
        ("Asosiy", {
            'fields': ('transport_type', 'icon', 'order', 'badge_style')
        }),
        ("Manzillar", {
            'fields': (
                ('from_location_uz', 'from_location_en', 'from_location_ru'),
                ('to_location_uz',   'to_location_en',   'to_location_ru'),
            )
        }),
        ("Narx va vaqt", {
            'fields': (('price_min', 'price_max'), ('duration_min', 'duration_max'))
        }),
        ("Belgilar (badge)", {
            'fields': ('badge_uz', 'badge_en', 'badge_ru')
        }),
        ("Tavsif", {
            'fields': ('description_uz', 'description_en', 'description_ru'),
            'classes': ('wide',)
        }),
    )
