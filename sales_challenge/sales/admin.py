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
admin.site.register(Client, ReadOnlyModelAdmin)
admin.site.register(Product, ReadOnlyModelAdmin)
admin.site.register(Merchant, ReadOnlyModelAdmin)
