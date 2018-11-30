from django.db import models


class BaseModel(models.Model):
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class Client(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return '{name}'.format(name=self.name)


class Product(BaseModel):
    description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    merchant = models.ForeignKey('Merchant', null=True, on_delete=models.CASCADE)

    def __str__(self):
        if self.merchant:
            return '{description}: R${price}, {merchant}'.format(description=self.description, price=self.price, merchant=self.merchant.name)
        return '{description}: R${price} '.format(description=self.description, price=self.price)


class Merchant(BaseModel):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)

    def __str__(self):
        return '{name}'.format(name=self.name)


class Transaction(BaseModel):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    purchase_count = models.IntegerField()

    def __str__(self):
        return '#{amount} of {product}'.format(product=self.product.description, amount=self.purchase_count)

