# Generated by Django 5.0.2 on 2025-03-22 05:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_remove_product_is_new_remove_product_is_sale'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='color_code',
        ),
    ]
