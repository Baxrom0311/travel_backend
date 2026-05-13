from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, UserFavorite


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'full_name', 'avatar_preview', 'language', 'is_verified', 'is_staff', 'created_at']
    list_display_links = ['email']
    list_filter = ['is_staff', 'is_superuser', 'is_verified', 'is_active', 'language']
    search_fields = ['email', 'first_name', 'last_name', 'phone']
    ordering = ['-created_at']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Profile', {'fields': ('first_name', 'last_name', 'avatar', 'phone', 'country', 'bio', 'language')}),
        ('Permissions', {'fields': ('is_active', 'is_verified', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'last_seen', 'created_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name'),
        }),
    )
    readonly_fields = ['created_at', 'last_seen']

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="32" height="32" style="object-fit:cover;border-radius:50%;"/>', obj.avatar.url)
        return "—"
    avatar_preview.short_description = "Avatar"


@admin.register(UserFavorite)
class UserFavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'favorite_type', 'object_id', 'created_at']
    list_filter = ['favorite_type', 'created_at']
    search_fields = ['user__email']
    readonly_fields = ['created_at']
