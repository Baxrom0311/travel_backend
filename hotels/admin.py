from django.contrib import admin
from django.utils.html import format_html
from .models import Hotel, HotelImage, Amenity, ContactMessage, Booking


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ['icon', 'name_uz', 'name_en', 'name_ru']
    search_fields = ['name_uz', 'name_en']


class HotelImageInline(admin.TabularInline):
    model       = HotelImage
    extra       = 3
    fields      = ['image', 'is_cover', 'order', 'preview']
    readonly_fields = ['preview']

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="60" style="border-radius:6px;" />', obj.image.url)
        return "—"
    preview.short_description = "Ko'rinish"


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display  = ['name', 'city', 'stars_display', 'rating', 'price_per_night', 'is_featured', 'cover_preview']
    list_display_links = ['name']  # Nom bosilganda tahrirlash ochiladi
    list_filter   = ['city', 'stars', 'is_featured']
    search_fields = ['name', 'name_en', 'name_ru', 'address', 'address_en', 'address_ru']
    list_editable = ['is_featured']
    filter_horizontal = ['amenities']
    inlines       = [HotelImageInline]

    fieldsets = (
        ("Asosiy ma'lumot", {
            'fields': ('name', 'name_en', 'name_ru', 'city', 'stars', 'rating', 'price_per_night', 'is_featured')
        }),
        ("Manzil", {
            'fields': ('address', 'address_en', 'address_ru')
        }),
        ("Joylashuv", {
            'fields': ('latitude', 'longitude', 'google_maps_url')
        }),
        ("Tavsif (ko'p tillik)", {
            'fields': ('description_uz', 'description_en', 'description_ru'),
            'classes': ('wide',)
        }),
        ("Qulayliklar", {
            'fields': ('amenities',)
        }),
    )

    def stars_display(self, obj):
        return '★' * obj.stars
    stars_display.short_description = "Yulduzlar"

    def cover_preview(self, obj):
        cover = obj.cover_image
        if cover:
            return format_html('<img src="{}" height="50" style="border-radius:4px;" />', cover.image.url)
        return "—"
    cover_preview.short_description = "Rasm"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display  = ['name', 'email', 'created_at', 'is_read']
    list_filter   = ['is_read']
    readonly_fields = ['name', 'email', 'message', 'created_at']
    list_editable = ['is_read']

    def has_add_permission(self, request):
        return False


# Admin site customization
admin.site.site_header = "🏛️ Visit Khorezm — Admin"
admin.site.site_title  = "Visit Khorezm Admin"
admin.site.index_title = "Boshqaruv paneli"


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['guest_name', 'hotel', 'check_in', 'check_out', 'status', 'total_price', 'created_at']
    list_filter = ['status', 'hotel__city']
    search_fields = ['guest_name', 'guest_phone', 'hotel__name']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at', 'total_price']
