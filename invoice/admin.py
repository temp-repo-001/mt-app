from django.contrib import admin

# Register your models here.
from .models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "invoice_number",
        "client_name",
        "client_email",
        "project_name",
        "amount",
        "paid",
    ]
    list_display_links = ["id", "invoice_number"]
    search_fields = [
        "id",
        "invoice_number",
        "client_name",
        "client_email",
        "project_name",
        "amount",
        "paid",
    ]
    exclude = ["id", "invoice_number"]
