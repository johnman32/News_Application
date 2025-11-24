from django.contrib import admin
from .models import Article, Newsletter, APIClient

admin.site.register(Article)
admin.site.register(Newsletter)


@admin.register(APIClient)
class APIClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'api_key', 'is_active', 'created_at']
    readonly_fields = ['api_key', 'created_at']
    filter_horizontal = ['subscribed_journalists', 'subscribed_publishers']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'api_key']
