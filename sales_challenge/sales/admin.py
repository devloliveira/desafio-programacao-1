from django import forms
from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.db.models import Count, Sum
from .parser import SalesParser
from .importer import SalesImporter
from .models import (
    Client,
    Product,
    Merchant,
    Transaction,
    SalesFile
)


class ReadOnlyModelAdmin(admin.ModelAdmin):

    def has_add_permission(self, *args, **kwargs):
        return False


class SalesFileForm(forms.ModelForm):

    class Meta:
        model = SalesFile
        fields = ('saved_file',)


class SalesFileAdmin(admin.ModelAdmin):
    form = SalesFileForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def has_delete_permission(self, *args, **kwargs):
        return False

    # Overriding the save model
    def save_model(self, request, obj, form, change):
        sales_data = obj.saved_file.read().decode('utf-8')
        parser = SalesParser(sales_data)
        sales_objects = parser.get_data()
        importer = SalesImporter(sales_objects)
        importer.run()

        return None

    def get_urls(self):
        urls = super().get_urls()
        print(urls)
        return urls

class TransactionChangeList(ChangeList):
    def get_results(self, *args, **kwargs):
        super().get_results(*args, **kwargs)

        gross_revenue = 0
        for transaction in self.result_list:
            gross_revenue += transaction.product.price * transaction.purchase_count

        self.gross_revenue = gross_revenue


class TransactionModelAdmin(admin.ModelAdmin):
    change_list_template = 'change_list.html'

    def get_changelist(self, request):
        return TransactionChangeList
admin.site.register(Client, ReadOnlyModelAdmin)
admin.site.register(Product, ReadOnlyModelAdmin)
admin.site.register(Merchant, ReadOnlyModelAdmin)
admin.site.register(Transaction, TransactionModelAdmin)
admin.site.register(SalesFile, SalesFileAdmin)
