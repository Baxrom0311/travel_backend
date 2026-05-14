from django.contrib import admin
from django.utils.html import format_html
from .models import Testimonial


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'role', 'rating', 'is_active', 'is_featured', 'order', 'avatar_preview')
    list_display_links = ('name',)
    list_filter = ('is_active', 'is_featured', 'rating', 'country')
    list_editable = ('order', 'is_active', 'is_featured')
    search_fields = ('name', 'country', 'text_uz', 'text_en')
    readonly_fields = ('created_at', 'avatar_preview')
    
    fieldsets = (
        ("Ma'lumot", {
            'fields': ('name', 'country', 'role', 'rating', 'avatar', 'avatar_preview'),
        }),
        ('Sharh matni', {
            'fields': ('text_uz', 'text_en', 'text_ru'),
        }),
        ('Sozlamalar', {
            'fields': ('is_active', 'is_featured', 'order', 'created_at'),
        }),
    )
    
    def avatar_preview(self, obj):
        if obj.avatar:
            try:
                return format_html('<img src="{}" style="height:60px;border-radius:50%"/>', obj.avatar.url)
            except Exception:
                pass
        return "-"
    avatar_preview.short_description = "Preview"
