# Generated by Django 4.0 on 2023-01-12 09:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_alter_review_product_carts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carts',
            name='qty',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)]),
        ),
    ]
