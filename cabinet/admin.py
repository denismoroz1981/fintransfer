from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin


# Register your models here.
from .models import Business, Entity, Vendor, Invoice, BKLimit

admin.site.register(Business)
admin.site.register(Entity)
admin.site.register(Vendor)
#admin.site.register(Invoice)
admin.site.register(BKLimit)

class InvoiceResource(resources.ModelResource):

    class Meta:
        model = Invoice
        fields = ("id","sap_entity_code","sap_vendor_code","i_vendor_code","i_vendor_name","vendor_contract_number","doc_date","doc_amount","doc_currency","doc_duedate","vendor_document_code","doc_payment_block")

class InvoiceAdmin(ImportExportModelAdmin):
    resource_class = InvoiceResource

admin.site.register(Invoice,InvoiceAdmin)