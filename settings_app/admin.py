from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from .models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Singleton admin - add/delete yo'q, faqat change."""

    fieldsets = (
        ('🗺️ Xarita sozlamalari', {
            'fields': ('map_provider', 'map_dark_provider', 'map_default_zoom'),
            'description': 'Siz tanlagan xarita butun saytda ko\'rsatiladi (barcha foydalanuvchilar uchun)',
        }),
        ('🌐 Sayt ma\'lumotlari', {
            'fields': ('site_name', 'site_tagline', 'site_description'),
        }),
        ('📞 Aloqa', {
            'fields': ('contact_email', 'contact_phone', 'contact_address'),
        }),
        ('🔗 Ijtimoiy tarmoqlar', {
            'fields': ('facebook_url', 'instagram_url', 'youtube_url', 'telegram_url'),
            'classes': ('collapse',),
        }),
        ('⚠️ Nazorat rejimi', {
            'fields': ('maintenance_mode', 'maintenance_message'),
            'classes': ('collapse',),
        }),
    )

    def has_add_permission(self, request):
        # Only allow adding if no instance exists
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        # Redirect list view to the singleton edit page
        obj, _ = SiteSettings.objects.get_or_create(pk=1)
        return redirect(reverse('admin:settings_app_sitesettings_change', args=[obj.pk]))
