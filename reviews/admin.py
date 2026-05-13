from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'content_object', 'rating', 'is_approved', 'created_at']
    list_display_links = ['name']
    list_filter = ['is_approved', 'rating', 'content_type', 'created_at']
    list_editable = ['is_approved']
    search_fields = ['name', 'email', 'comment']
    readonly_fields = ['created_at', 'content_object']
    
    fieldsets = (
        ('Target', {'fields': ('content_type', 'object_id', 'content_object')}),
        ('Reviewer', {'fields': ('name', 'email', 'country')}),
        ('Review', {'fields': ('rating', 'title', 'comment')}),
        ('Status', {'fields': ('is_approved', 'created_at')}),
    )
