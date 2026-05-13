from django.contrib import admin
from django.utils.html import format_html
from .models import Restaurant, RestaurantImage, Cuisine


class RestaurantImageInline(admin.TabularInline):
    model = RestaurantImage
    extra = 1
    fields = ['image', 'preview', 'is_cover', 'order']
    readonly_fields = ['preview']

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="70" style="object-fit:cover;border-radius:4px;"/>', obj.image.url)
        return "—"


@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    list_display = ['icon', 'name_uz', 'name_en', 'name_ru']
    list_display_links = ['name_uz']
    search_fields = ['name_uz']


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'cover_preview', 'city', 'price_range', 'rating', 'is_featured']
    list_display_links = ['name']
    list_filter = ['city', 'price_range', 'is_featured', 'is_halal']
    list_editable = ['is_featured']
    search_fields = ['name', 'name_en', 'address']
    filter_horizontal = ['cuisines']
    inlines = [RestaurantImageInline]

    fieldsets = (
        ('Asosiy', {'fields': ('name', 'name_en', 'name_ru', 'cuisines', 'city', 'price_range', 'rating', 'is_featured')}),
        ('Tavsif', {'fields': ('description_uz', 'description_en', 'description_ru')}),
        ('Manzil', {'fields': ('address', 'address_en', 'address_ru', 'latitude', 'longitude')}),
        ('Kontakt', {'fields': ('phone', 'website', 'working_hours')}),
        ('Xususiyatlar', {'fields': ('has_wifi', 'has_parking', 'has_outdoor_seating', 'is_halal', 'is_vegetarian_friendly')}),
    )

    def cover_preview(self, obj):
        cover = obj.cover_image
        if cover:
            return format_html('<img src="{}" width="60" height="40" style="object-fit:cover;border-radius:4px;"/>', cover.image.url)
        return "—"
    cover_preview.short_description = "Rasm"
