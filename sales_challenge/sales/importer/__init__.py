
from ..models import (
    Client,
    Product,
    Merchant,
    Transaction
)


class SalesImporter(object):

    def __init__(self, sales_objects):
        self.sales_objects = sales_objects

    def run(self):
        for sale_object in self.sales_objects:
            client = Client.objects.get_or_create(name=sale_object.purchaser_name)
            merchant, new_merchant = Merchant.objects.get_or_create(name=sale_object.merchant_name, address=sale_object.merchant_address)
            product, new_product = Product.objects.get_or_create(price=sale_object.item_price, description=sale_object.item_description, merchant=merchant)
            transaction = Transaction.objects.create(product=product, purchase_count=sale_object.purchase_count)
