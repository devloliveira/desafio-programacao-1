import re

class SaleObject(object):

    def __init__(self, args):
        self.purchaser_name = args[0]
        self.item_description = args[1]
        self.item_price = float(args[2])
        self.purchase_count = int(args[3])
        self.merchant_address = args[4]
        self.merchant_name = args[5]

    def get_revenue(self):
        return self.item_price * self.purchase_count

    def __len__(self):
        return 6

class BaseParser(object):

    def __init__(self, data, column_sep):
        self.data = data
        self.column_sep = column_sep

    def normalize(self, line):
        return re.sub(r'{}+'.format(self.column_sep), self.column_sep, line)

    def get_columns(self):
        header_line = self.data.split('\n')[0]
        return self.normalize(header_line).split(self.column_sep)

    def extract_line_data(self, line):
        return self.normalize(line).split(self.column_sep)

    def get_data(self):
        raise NotImplementedError


class SalesParser(BaseParser):
    COLUMN_SEP = '\t'

    def __init__(self, sales_data):
        super(SalesParser, self).__init__(
            sales_data, SalesParser.COLUMN_SEP)

    def get_data(self):
        lines = self.data.split('\n')[1:]
        formated_data = list()
        for i, line in enumerate(lines):
            if line:
                data = self.extract_line_data(line)
                formated_data.append(SaleObject(data))

        return formated_data

    @staticmethod
    def get_gross_revenue(processed_sales):
        return sum([sale_data.get_revenue() for sale_data in processed_sales])
