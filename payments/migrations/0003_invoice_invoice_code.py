# Generated by Django 3.1.3 on 2021-04-05 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_invoice_payment_complete'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='invoice_code',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]