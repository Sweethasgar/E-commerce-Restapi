# Generated by Django 4.0 on 2023-01-13 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_orders'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='status',
            field=models.CharField(choices=[('order_placed', 'order_placed'), ('delivered', 'delivered')], default='order_placed', max_length=20),
        ),
    ]
