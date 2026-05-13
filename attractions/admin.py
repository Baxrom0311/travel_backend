from django.contrib import admin
from django.utils.html import format_html
from .models import Attraction, AttractionImage


class AttractionImageInline(admin.TabularInline):
    model = AttractionImage
    extra = 1
    fields = ['image', 'image_preview', 'caption_uz', 'is_cover', 'order']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="70" style="object-fit:cover;border-radius:4px;"/>',
                obj.image.url
            )
        return "—"
    image_preview.short_description = "Ko'rinish"


@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    list_display = ['icon', 'name_uz', 'cover_preview', 'images_count', 'is_featured', 'order']
    list_display_links = ['name_uz']
    list_editable = ['is_featured', 'order']
    list_filter = ['is_featured']
    search_fields = ['name_uz', 'name_en', 'name_ru']
    inlines = [AttractionImageInline]
    
    fieldsets = (
        ('Asosiy', {
            'fields': ('icon', 'name_uz', 'name_en', 'name_ru')
        }),
        ('Tavsif', {
            'fields': ('description_uz', 'description_en', 'description_ru')
        }),
        ('Tarix', {
            'fields': ('history_uz', 'history_en', 'history_ru'),
            'classes': ('collapse',)
        }),
        ('Media', {
            'fields': ('video_url',)
        }),
        ('Joylashuv', {
            'fields': ('latitude', 'longitude')
        }),
        ('Qo\'shimcha', {
            'fields': ('working_hours', 'entrance_fee', 'is_featured', 'order')
        }),
    )

    def cover_preview(self, obj):
        cover = obj.cover_image
        if cover:
            return format_html(
                '<img src="{}" width="80" height="50" style="object-fit:cover;border-radius:4px;"/>',
                cover.image.url
            )
        return "—"
    cover_preview.short_description = "Asosiy rasm"

    def images_count(self, obj):
        count = obj.images.count()
        return f"{count} ta"
    images_count.short_description = "Rasmlar"


@admin.register(AttractionImage)
class AttractionImageAdmin(admin.ModelAdmin):
    list_display = ['attraction', 'image_preview', 'is_cover', 'order']
    list_filter = ['attraction', 'is_cover']
    list_editable = ['is_cover', 'order']

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="70" style="object-fit:cover;border-radius:4px;"/>',
                obj.image.url
            )
        return "—"
    image_preview.short_description = "Rasm"
