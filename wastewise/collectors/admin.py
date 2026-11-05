from django.contrib import admin
from .models import Zone, Collector
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class ZoneAdmin(ImportExportModelAdmin):
    list_display = [
        'id', 'name', 'description'
    ]


class CollectorAdmin(ImportExportModelAdmin):
    list_display = [
        'id', 'user', 'phone_number', 'zone', 'status', 'is_available', 'created_at'
    ]


admin.site.register(Zone, ZoneAdmin)
admin.site.register(Collector, CollectorAdmin)