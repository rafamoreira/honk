from django.contrib import admin

from circus.models import Honk


class HonkAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at', 'seen')


admin.site.register(Honk, HonkAdmin)
