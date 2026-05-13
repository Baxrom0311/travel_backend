from django.contrib import admin
from django.utils.html import format_html
from .models import Tour, TourImage


class TourImageInline(admin.TabularInline):
    model = TourImage
    extra = 1


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ['title_uz', 'cover_preview', 'price', 'duration', 'difficulty', 'is_featured', 'is_active']
    list_display_links = ['title_uz']
    list_filter = ['difficulty', 'is_featured', 'is_active']
    list_editable = ['is_featured', 'is_active']
    prepopulated_fields = {'slug': ('title_uz',)}
    inlines = [TourImageInline]
    search_fields = ['title_uz', 'title_en']

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" width="60" height="40" style="object-fit:cover;border-radius:4px;"/>', obj.cover_image.url)
        return "—"
