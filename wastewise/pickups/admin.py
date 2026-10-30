from django.contrib import admin
from .models import pickup_request  
from import_export.admin import ImportExportModelAdmin
# Register your models here.
# class AuthorAdmin(admin.ModelAdmin):
#     list_display = [
#         "id",'first_name','last_name','dob','year_of_death'
#     ]
class AuthorAdmin(ImportExportModelAdmin):
    list_display = [
        "id",'user_id','collector_id','request_date','request_status','collection_date'
    ]

admin.site.register(pickup_request,AuthorAdmin)
