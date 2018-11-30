from django.contrib import admin
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
