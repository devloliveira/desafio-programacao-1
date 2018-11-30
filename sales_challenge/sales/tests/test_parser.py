from django.test import TestCase
from ..parser import SalesParser


class ParserTest(TestCase):

    def test_get_columns_should_consider_a_TAB_separated_string(self):
        sales_data = '''purchaser name\titem description\titem price\tpurchase count\tmerchant address\tmerchant name
        '''
        expected = ('purchaser name', 'item description', 'item price', 'purchase count', 'merchant address', 'merchant name')
        returned = SalesParser(sales_data).get_columns()

        self.assertEqual(6, len(returned))
        self.assertEqual(set(expected), set(returned))

    def test_get_columns_should_work_as_expected_when_multiple_TABS_are_found_between_two_fields(self):
        sales_data = '''purchaser name\t\t\titem description\t\titem price\tpurchase count\t\tmerchant address\t\t\t\tmerchant name
        '''
        expected = ('purchaser name', 'item description', 'item price', 'purchase count', 'merchant address', 'merchant name')
        returned = SalesParser(sales_data).get_columns()

        self.assertEqual(6, len(returned))
        self.assertEqual(set(expected), set(returned))

    def test_get_data_should_return_the_correct_number_of_lines(self):
        data_list = [
            'purchaser name\t\t\titem description\t\titem price\tpurchase count\t\tmerchant address\t\t\t\tmerchant name',
            'Dummy Purchaser\t\tDummy Item Description\t10.0\t\t\t3\t\tDummy Fake St\t\t\t\tDummy Awesome Shop\t',
            'Dummy Purchaser\t\tDummy Item Description\t10.0\t\t\t3\t\tDummy Fake St\t\t\t\tDummy Awesome Shop\t',
            'Dummy Purchaser\t\tDummy Item Description\t10.0\t\t\t3\t\tDummy Fake St\t\t\t\tDummy Awesome Shop\t',
        ]
        sales_data = '\n'.join(data_list)
        returned = SalesParser(sales_data).get_data()

        self.assertEqual(3, len(returned))

    def test_get_data_should_ignore_the_last_empty_line(self):
        data_list = [
            'purchaser name\t\t\titem description\t\titem price\tpurchase count\t\tmerchant address\t\t\t\tmerchant name',
            'Dummy Purchaser\t\tDummy Item Description\t10.0\t\t\t3\t\tDummy Fake St\t\t\t\tDummy Awesome Shop\t',
            'Dummy Purchaser\t\tDummy Item Description\t10.0\t\t\t3\t\tDummy Fake St\t\t\t\tDummy Awesome Shop\t',
            'Dummy Purchaser\t\tDummy Item Description\t10.0\t\t\t3\t\tDummy Fake St\t\t\t\tDummy Awesome Shop\t',
            '',
        ]
        sales_data = '\n'.join(data_list)
        returned = SalesParser(sales_data).get_data()

        self.assertEqual(3, len(returned))

    def test_get_data_should_return_the_correct_formated_information(self):
        data_list = [
            'purchaser name\t\t\titem description\t\titem price\tpurchase count\t\tmerchant address\t\t\t\tmerchant name',
            'Dummy Purchaser\tDummy Item Description\t10.0\t3\tDummy Fake St\tDummy Awesome Shop',
        ]
        sales_data = '\n'.join(data_list)
        returned = SalesParser(sales_data).get_data()

        self.assertEqual(1, len(returned))
        self.assertEqual(6, len(returned[0]))
        self.assertEqual('Dummy Purchaser', returned[0].purchaser_name)
        self.assertEqual('Dummy Item Description', returned[0].item_description)
        self.assertEqual(10.0, returned[0].item_price)
        self.assertEqual(3, returned[0].purchase_count)
        self.assertEqual('Dummy Fake St', returned[0].merchant_address)
        self.assertEqual('Dummy Awesome Shop', returned[0].merchant_name)

    def test_get_data_should_return_the_expected_data_even_if_there_are_multiple_TABS_between_fields(self):
        data_list = [
            'purchaser name\t\t\titem description\t\titem price\tpurchase count\t\tmerchant address\t\t\t\tmerchant name',
            'Dummy Purchaser\t\tDummy Item Description\t10.0\t\t\t3\t\tDummy Fake St\t\t\t\tDummy Awesome Shop\t',
        ]
        sales_data = '\n'.join(data_list)
        returned = SalesParser(sales_data).get_data()

        self.assertEqual(1, len(returned))
        self.assertEqual(6, len(returned[0]))
        self.assertEqual('Dummy Purchaser', returned[0].purchaser_name)
        self.assertEqual('Dummy Item Description', returned[0].item_description)
        self.assertEqual(10.0, returned[0].item_price)
        self.assertEqual(3, returned[0].purchase_count)
        self.assertEqual('Dummy Fake St', returned[0].merchant_address)
        self.assertEqual('Dummy Awesome Shop', returned[0].merchant_name)

    def test_get_data_should_return_the_expected_number_of_fields_even_when_line_with_special_characters_are_found(self):
        data_list = [
            'purchaser name\t\t\titem description\t\titem price\tpurchase count\t\tmerchant address\t\t\t\tmerchant name',
            'Dummy Purchaser\t\tR$Dummy Item Description\t10.0\t\t\t3\t\tDummy Fake St\t\t\t\tDummy Awesome Shop\t',
            "Dummy Purchaser\t\tDummy's Item Description\t10.0\t\t\t3\t\tDummy Fake St\t\t\t\tDummy Awesome Shop\t",
            "João Silva\t\tDummy's Item Description\t10.0\t\t\t3\t\tDummy Fake St\t\t\t\tDummy Awesome Shop\t",
        ]
        sales_data = '\n'.join(data_list)
        returned = SalesParser(sales_data).get_data()

        self.assertEqual(3, len(returned))
        self.assertEqual(6, len(returned[0]))
        self.assertEqual(6, len(returned[1]))
        self.assertEqual(6, len(returned[2]))


    def test_get_data_objects_should_correctly_calculate_the_sale_revenue(self):
        data_list = [
            'purchaser name\t\t\titem description\t\titem price\tpurchase count\t\tmerchant address\t\t\t\tmerchant name',
            'Dummy Purchaser\t\tDummy Item Description\t10.0\t\t\t3\t\tDummy Fake St\t\t\t\tDummy Awesome Shop\t',
        ]
        sales_data = '\n'.join(data_list)
        returned = SalesParser(sales_data).get_data()

        self.assertEqual(30.0, returned[0].get_revenue())

    def test_get_gross_revenue_should_return_the_expected_calculated_value(self):
        data_list = [
            'purchaser name\t\t\titem description\t\titem price\tpurchase count\t\tmerchant address\t\t\t\tmerchant name',
            'Dummy Purchaser\t\tDummy Item Description\t10.0\t\t\t2\t\tDummy Fake St\t\t\t\tDummy Awesome Shop\t',
            'Dummy Purchaser\t\tDummy Item Description\t2.0\t\t\t3\t\tDummy Fake St\t\t\t\tDummy Awesome Shop\t',
            'Dummy Purchaser\t\tDummy Item Description\t0.0\t\t\t5\t\tDummy Fake St\t\t\t\tDummy Awesome Shop\t',
        ]
        sales_data = '\n'.join(data_list)
        returned = SalesParser(sales_data).get_data()

        self.assertEqual(20 + 6 + 0, SalesParser.get_gross_revenue(returned))
