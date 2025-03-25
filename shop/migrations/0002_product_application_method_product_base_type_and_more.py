# Generated by Django 5.0.2 on 2025-03-21 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='application_method',
            field=models.CharField(blank=True, max_length=200, verbose_name='Способ нанесения'),
        ),
        migrations.AddField(
            model_name='product',
            name='base_type',
            field=models.CharField(blank=True, max_length=100, verbose_name='Тип основы'),
        ),
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.CharField(blank=True, max_length=100, verbose_name='Бренд'),
        ),
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.CharField(blank=True, max_length=50, verbose_name='Цвет'),
        ),
        migrations.AddField(
            model_name='product',
            name='color_code',
            field=models.CharField(blank=True, max_length=20, verbose_name='Код цвета'),
        ),
        migrations.AddField(
            model_name='product',
            name='country_of_origin',
            field=models.CharField(blank=True, max_length=100, verbose_name='Страна производитель'),
        ),
        migrations.AddField(
            model_name='product',
            name='coverage',
            field=models.CharField(blank=True, max_length=100, verbose_name='Расход (м²/л)'),
        ),
        migrations.AddField(
            model_name='product',
            name='drying_time',
            field=models.CharField(blank=True, max_length=100, verbose_name='Время высыхания'),
        ),
        migrations.AddField(
            model_name='product',
            name='gloss_level',
            field=models.CharField(blank=True, max_length=50, verbose_name='Уровень глянца'),
        ),
        migrations.AddField(
            model_name='product',
            name='is_new',
            field=models.BooleanField(default=True, verbose_name='Новинка'),
        ),
        migrations.AddField(
            model_name='product',
            name='is_sale',
            field=models.BooleanField(default=False, verbose_name='Распродажа'),
        ),
        migrations.AddField(
            model_name='product',
            name='minimum_order_quantity',
            field=models.IntegerField(default=1, verbose_name='Минимальное количество для заказа'),
        ),
        migrations.AddField(
            model_name='product',
            name='safety_instructions',
            field=models.TextField(blank=True, verbose_name='Инструкция по безопасности'),
        ),
        migrations.AddField(
            model_name='product',
            name='sale_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Цена по акции'),
        ),
        migrations.AddField(
            model_name='product',
            name='surface_type',
            field=models.CharField(blank=True, max_length=200, verbose_name='Тип поверхности'),
        ),
        migrations.AddField(
            model_name='product',
            name='technical_specifications',
            field=models.TextField(blank=True, verbose_name='Технические характеристики'),
        ),
        migrations.AddField(
            model_name='product',
            name='unit',
            field=models.CharField(default='шт', max_length=20, verbose_name='Единица измерения'),
        ),
        migrations.AddField(
            model_name='product',
            name='usage_instructions',
            field=models.TextField(blank=True, verbose_name='Инструкция по применению'),
        ),
        migrations.AddField(
            model_name='product',
            name='volume',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Объем (л)'),
        ),
        migrations.AddField(
            model_name='product',
            name='warranty_months',
            field=models.IntegerField(blank=True, null=True, verbose_name='Гарантия (месяцев)'),
        ),
        migrations.AddField(
            model_name='product',
            name='weight',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Вес (кг)'),
        ),
    ]
