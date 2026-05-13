from django.contrib import admin
from django.utils.html import format_html
from .models import Event, EventImage


class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 1


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title_uz', 'cover_preview', 'start_date', 'location_uz', 'is_featured', 'is_active']
    list_display_links = ['title_uz']
    list_filter = ['is_featured', 'is_active', 'start_date']
    list_editable = ['is_featured', 'is_active']
    search_fields = ['title_uz', 'title_en']
    inlines = [EventImageInline]
    date_hierarchy = 'start_date'

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" width="80" height="50" style="object-fit:cover;border-radius:4px;"/>', obj.cover_image.url)
        return "—"
    cover_preview.short_description = "Rasm"
