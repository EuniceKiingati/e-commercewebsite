# Generated by Django 4.1b1 on 2022-07-14 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0005_remove_customer_birth_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="date_ordered",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
