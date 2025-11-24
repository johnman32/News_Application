from django.contrib import admin
from .models import Publisher
from django.contrib.auth.models import User


class PublisherAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    list_display_links = ['id', 'name']

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "users":
            kwargs["queryset"] = User.objects.filter(profile__role__in=['editor', 'journalist'])
        return super().formfield_for_manytomany(db_field, request, **kwargs)


admin.site.register(Publisher, PublisherAdmin)
