# Generated by Django 2.1 on 2018-11-28 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_client_merchant'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='merchant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.Merchant'),
        ),
    ]
