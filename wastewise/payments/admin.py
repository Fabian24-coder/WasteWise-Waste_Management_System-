from django.contrib import admin
from .models import Payment
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class PaymentAdmin(ImportExportModelAdmin):
    list_display = [
        'id', 'request', 'amount', 'payment_method', 'payment_status', 'transaction_reference', 'payment_date'
    ]


admin.site.register(Payment, PaymentAdmin)