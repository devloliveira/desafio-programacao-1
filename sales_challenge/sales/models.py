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
