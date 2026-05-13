from django.contrib import admin
from django.utils.html import format_html
from .models import News, NewsImage


class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 1


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title_uz', 'cover_preview', 'published_at', 'is_featured', 'is_published']
    list_display_links = ['title_uz']
    list_filter = ['is_featured', 'is_published', 'published_at']
    list_editable = ['is_featured', 'is_published']
    search_fields = ['title_uz', 'title_en', 'content_uz']
    prepopulated_fields = {'slug': ('title_uz',)}
    inlines = [NewsImageInline]
    date_hierarchy = 'published_at'

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" width="80" height="50" style="object-fit:cover;border-radius:4px;"/>', obj.cover_image.url)
        return "—"
    cover_preview.short_description = "Rasm"
