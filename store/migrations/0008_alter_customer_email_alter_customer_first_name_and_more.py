# Generated by Django 4.1b1 on 2022-07-17 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0007_product_in_stock_alter_orderitem_product"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="email",
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="customer",
            name="first_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="customer",
            name="last_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="customer",
            name="phone",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
