# Generated by Django 5.2.1 on 2025-06-07 09:41

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Product_category',
            new_name='ProductCategory',
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('text', models.TextField(verbose_name='Описание')),
                ('photo', models.ImageField(upload_to='products/', verbose_name='Фото товара')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена')),
                ('count', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Количество на складе')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='main.productcategory')),
                ('producer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='main.producer')),
            ],
            options={
                'verbose_name_plural': 'Товары',
            },
        ),
    ]
