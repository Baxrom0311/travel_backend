from django.contrib import admin
from .models import NewsletterSubscription


@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['email', 'language', 'is_active', 'subscribed_at']
    list_display_links = ['email']
    list_filter = ['is_active', 'language', 'subscribed_at']
    list_editable = ['is_active']
    search_fields = ['email']
    readonly_fields = ['subscribed_at', 'unsubscribed_at']
