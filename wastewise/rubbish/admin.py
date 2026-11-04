from django.contrib import admin
from .models import RubbishDetail


@admin.register(RubbishDetail)
class RubbishDetailAdmin(admin.ModelAdmin):
    list_display = ('waste_id', 'name', 'category',
                    'rate', 'unit', 'is_active')
    list_filter = ('category', 'is_hazardous', 'is_recyclable', 'is_active')
    search_fields = ('name', 'description')
