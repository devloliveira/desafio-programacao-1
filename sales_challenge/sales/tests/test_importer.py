from django.test import TestCase
from mock import MagicMock
from ..importer import SalesImporter
from ..models import (
    Client,
    Merchant,
    Product,
    Transaction,
)


class ImporterTest(TestCase):

    def setUp(self):
        self.mockSaleObject = MagicMock()
        self.mockSaleObject.purchaser_name = 'Dummy purchaser name'
        self.mockSaleObject.item_description = 'Dummy item description'
        self.mockSaleObject.item_price = 123.45
        self.mockSaleObject.purchase_count = 3
        self.mockSaleObject.merchant_address = 'Dummy merchant address'
        self.mockSaleObject.merchant_name = 'Dummy merchant name'

    def test_should_save_a_new_client_when_one_does_not_exists(self):
        SalesImporter([self.mockSaleObject]).run()

        client_queryset = Client.objects.all()
        self.assertEqual(1, client_queryset.count())
        self.assertEqual('Dummy purchaser name', client_queryset[0].name)

    def test_should_not_save_a_new_client_when_one_already_exists(self):
        Client.objects.create(name='Dummy purchaser name')
        SalesImporter([self.mockSaleObject]).run()

        client_queryset = Client.objects.all()
        self.assertEqual(1, client_queryset.count())
        self.assertEqual('Dummy purchaser name', client_queryset[0].name)

    def test_should_save_a_new_merchant_when_one_does_not_exists(self):
        SalesImporter([self.mockSaleObject]).run()

        merchant_queryset = Merchant.objects.all()
        self.assertEqual(1, merchant_queryset.count())
        self.assertEqual('Dummy merchant name', merchant_queryset[0].name)

    def test_should_not_save_a_new_merchant_when_one_already_exists(self):
        Merchant.objects.create(name='Dummy merchant name', address='Dummy merchant address')
        SalesImporter([self.mockSaleObject]).run()

        merchant_queryset = Merchant.objects.all()
        self.assertEqual(1, merchant_queryset.count())
        self.assertEqual('Dummy merchant name', merchant_queryset[0].name)
        self.assertEqual('Dummy merchant address', merchant_queryset[0].address)

    def test_should_save_a_new_product_when_one_does_not_exists(self):
        SalesImporter([self.mockSaleObject]).run()

        product_queryset = Product.objects.all()
        self.assertEqual(1, product_queryset.count())
        self.assertEqual('Dummy item description', product_queryset[0].description)
        self.assertEqual(123.45, float(product_queryset[0].price))
        self.assertTrue(None != product_queryset[0].merchant)

    def test_should_not_save_a_new_product_when_one_already_exists(self):
        merchant = Merchant.objects.create(name='Dummy merchant name', address='Dummy merchant address')
        Product.objects.create(description='Dummy item description', price=123.45, merchant=merchant)
        SalesImporter([self.mockSaleObject]).run()

        product_queryset = Product.objects.all()
        self.assertEqual(1, product_queryset.count())
        self.assertEqual('Dummy item description', product_queryset[0].description)
        self.assertEqual(123.45, float(product_queryset[0].price))

    def test_should_save_the_sale_transaction_in_the_database(self):
        client = Client.objects.create(name='Dummy purchaser name')
        merchant = Merchant.objects.create(name='Dummy merchant name', address='Dummy merchant address')
        product = Product.objects.create(description='Dummy item description', price=123.45)

        SalesImporter([self.mockSaleObject]).run()

        transaction_queryset = Transaction.objects.all()
        self.assertEqual(1, transaction_queryset.count())
        self.assertEqual(123.45, float(transaction_queryset[0].product.price))
        self.assertEqual(3, transaction_queryset[0].purchase_count)
